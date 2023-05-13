# this file contains all the classes needed to be implemented to design the MDP solver

from typing import Dict
# this is just to refer to the data type Dictionary for readability in the following lines of code


class State:
    def __init__(self, val,g):  # a state object is characterized by a numerical value and boolean attribute goal
        self.state_val = val
        self.goal = g

    def __eq__(self, other):
        if isinstance(other, State):
            return self.state_val == other.state_val and self.goal == other.goal
        return False

    def __hash__(self):
        return hash((self.state_val, self.goal))

    def __str__(self):
        return f"State({self.state_val}, {self.goal})"


class Action:
    def __init__(self, name):  # an action object is characterized by a string
        self.action_name = name

    def __eq__(self, other):
        if isinstance(other, Action):
            return self.action_name == other.action_name
        return False

    def __hash__(self):
        return hash(self.action_name)

    def __str__(self):
        return f"Action({self.action_name})"


class Transition:
    def __init__(self, p: State, q: State, a: Action):
        # a transition object is characterized by two states and an action
        self.state_from = p
        self.state_to = q
        self.through = a

    def __eq__(self, other):
        if isinstance(other, Transition):
            return self.state_from == other.state_from and self.state_to == other.state_to and self.through == other.through
        return False

    def __hash__(self):
        return hash((self.state_from, self.state_to, self.through))

    def __str__(self):
        return f"Transition({self.state_from},{self.through} .{self.state_to})"


class Cost:
    def __init__(self, s: State, a: Action, C):
        # a cost is characterized by one state object , an action object  and a numerical value defining its cost
        self.through = a
        self.state_from = s
        self.cost = C

    def __eq__(self, other):
        if isinstance(other, Cost):
            return self.through == other.through and self.state_from == other.state_from and self.cost == other.cost
        return False

    def __hash__(self):
        return hash((self.through, self.state_from, self.cost))

    def __str__(self):
        return f"Cost({self.state_from}, {self.through}, {self.cost})"


class MDP:

    def __init__(self, S, T, A, C, IC):
        # characterized by a set of States, transitions, actions and costs objects
        self.States = S  # set of state objects
        self.Transitions = T  # dictionary: key is a transition and value a probability (Transition model)
        self.Actions = A  # set of action objects
        self.Costs = C  # set of cost objects
        self.ImmediateCosts = IC  # dictionary where each key is an action object and values its associated cost

    def PrintAll(self):
        print("Set of states: ")
        for s in self.States:
            print(s)
        print("Transition model: ")
        for k in self.Transitions:
            print(str(k) + " = " + str(self.Transitions[k]))
        print("Set of actions : ")
        for a in self.Actions:
            print(str(a))
        print("Immediate costs: ")
        for c in self.ImmediateCosts:
            print(str(c) + " = " + str(self.ImmediateCosts[c]))
        print("--------------")

    def ValueIteration(self):
        # solves the Bellman's Equations iteratively through the common fixed point method
        done = False
        iters = 0
        V = {key: 0 for key in self.States} # dictionary initialization where keys are states and values 0
        while not done:  # (later we will determine a stopping criteria)
            OldV = V.copy()
            for s in V:
                if not s.goal:
                    # set value for s to be Min(I_cost(a) + Sigma_all s' ( Transition(s,a,s')*V[s])
                    min = float('inf')  # initialize the min value as +infinity
                    for a in self.Actions:  # iterate over all the actions in the set of Actions of the MDP object...
                        v = self.ImmediateCosts[a]
                        for s_prime in self.States:
                            t = Transition(s, s_prime, a)
                            v += self.Transitions[t] * OldV[s_prime]
                        if v < min:
                            min = v  # new minimum found
                    # now, update the value of current state s on V dictionary...
                    V[s] = min
            if OldV == V:
                done = True
        return V  # in the end , the dictionary V contains the values for all the states in the MDP object.

    def OptimalPolicy(self):
        V = self.ValueIteration()
        OP = {s: None for s in self.States}
        for s in self.States:
            if not s.goal: #for all those states that are not goal states...
                min = float('inf')
                opt_action = None
                for a in self.Actions:
                    c = self.ImmediateCosts[a]
                    for s_prime in self.States:
                        # for each state in the set of states, loop through all actions and compute weighted sum of values
                        t = Transition(s, s_prime, a)
                        c += self.Transitions[t] * V[s_prime]
                    if c < min:
                        opt_action = a # update the optimal action found for the state s
                OP[s] = opt_action
        return OP  # in the end, the dictionary OP contains the optimal actions for all the sates in the MDP object




s1 = State(1,0)
s2 = State(2,0)
s3 = State(3,1)
S = {s2, s1, s3} #set of states
a = Action("right")
A = {a}
t1 = Transition(s1,s1,a)
t2 = Transition(s1,s2,a)
t3 = Transition(s1,s3,a)
t4 = Transition(s2,s1,a)
t5 = Transition(s2,s2,a)
t6 = Transition(s2,s3,a)
t7 = Transition(s3,s1,a)
t8 = Transition(s3,s2,a)
t9 = Transition(s3,s3,a)
IC = {a:1}
T = {t1:0.2, t2:0.8, t3:0, t4:0, t5:0.2, t6:0.8, t7:0.8, t8:0.0, t9:0.2}

my_mdp = MDP(S, T, A, None, IC)
my_mdp.PrintAll()
Values = my_mdp.ValueIteration()
Opt = my_mdp.OptimalPolicy()
for i in Values:
    print(str(i) + " = " + str(Values[i]))
for j in Opt:
    print(str(j) + " = " + str(Opt[j]))

