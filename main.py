from setUp import setUp_mdpSolver

file = input("Introduce name of file that contains your MDP problem: ")
basic_mdp = setUp_mdpSolver(file)
policy = basic_mdp.OptimalPolicy()

# Print the resulting policy
print("OPTIMAL POLICY :")
for state in policy:
    print(f"State: {state}, Action: {policy[state]}")
