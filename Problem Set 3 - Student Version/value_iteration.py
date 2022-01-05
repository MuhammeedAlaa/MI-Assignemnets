from typing import Dict
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[str, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {str(state):0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        if self.mdp.is_terminal(state):
            return 0
        actions = self.mdp.get_actions(state)
        res = []
        for action in actions:
            successors = self.mdp.get_successor(state, action)
            U = 0
            for successor in successors:
                U +=  successors[successor] * (self.mdp.get_reward(state, action, successor) +
                     self.discount_factor * self.utilities[successor.__str__()])
            res.append(U)
        max_item = float('-inf')
        for u in res:
            if max_item < u:
                max_item = u
        return max_item
    
    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: int = 1):
        states = self.mdp.get_states()
        for _ in range(iterations):
            temp_u = {}
            for state in states:
                 temp_u[state.__str__()] = self.compute_bellman(state)
            for state in states:
                self.utilities[state.__str__()] = temp_u[state.__str__()]
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        actions = self.mdp.get_actions(state)
        pi = []
        for action in actions:
            successors = self.mdp.get_successor(state, action)
            u_p = 0
            for successor in successors:
                u_p += successors[successor] * (self.mdp.get_reward(state, action, successor) +
                                                self.discount_factor * self.utilities[successor.__str__()])
            pi.append(u_p)
        max_item = 0
        for inx, u in enumerate(pi):
            if pi[max_item] < u:
                max_item = inx
        return actions[max_item]
    
    # Save the utilities to a json file
    def save(self, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(self.utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, file_path: str):
        with open(file_path, 'r') as f:
            self.utilities = json.load(f)
