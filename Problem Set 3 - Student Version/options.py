# This file contains the options that you should modify to solve Question 2

# we make living_reward more negative so he try to leave quickly so he take the short path to the first end
def question2_1():
    #TODO: Choose options that would lead to the desired results 
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -3.5
    }

def question2_2():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.3,
        "discount_factor": 0.35,
        "living_reward": 0
    }

# we make living_reward slitly negative so he try to leave from the far terminal state with quickest path
def question2_3():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -2
    }

def question2_4():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -0.03
    }

def question2_5():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 0.99,
        "living_reward": 100000
    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 0.99,
        "living_reward": -100000000000
    }
