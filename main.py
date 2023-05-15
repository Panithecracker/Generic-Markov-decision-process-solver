from setUp import setUp_mdpSolver
from mdp import State, Transition, Action, MDP

file = input("Introduce name of file that contains your MDP problem: ")
basic_mdp = setUp_mdpSolver(file)
policy = basic_mdp.OptimalPolicy()

#The user can provide the model data through a well formatted text file

print("OPTIMAL POLICY :")
for state in policy:
   print(f"{state} -> Optimal: {policy[state]}")

print('Contents have been successfully written in a file called "OptimalPolicy.txt" ')
basic_mdp.WriteOptimalPolicy(policy)
