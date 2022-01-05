# This file contains the options that you should modify to solve Question 2

# we make living_reward more negative so he try to leave quickly so he take the short path to the first end
def question2_1():
    #TODO: Choose options that would lead to the desired results 
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -3.5
    }

# we make living_reward 0 and make discount_factor slightly small and try to add noise on actions taken
def question2_2():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.3,
        "discount_factor": 0.35,
        "living_reward": 0
    }

# we make living_reward slightly negative so he try to leave from the far terminal state with quickest path
def question2_3():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -2
    }

# we make living_reward very small negative so he try to leave from the far terminal state with long path
def question2_4():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -0.03
    }

# we make the living_reward big postive and action is deterministic so that the agent will not go to a terminal state and it will keep moving to collect the postive reward
def question2_5():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 0.99,
        "living_reward": 100000
    }
# we make the living_reward big negative and action is deterministic so that the agent will try to skip the big penalty by go to any terminal state
def question2_6():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 0.99,
        "living_reward": -100000000000
    }
