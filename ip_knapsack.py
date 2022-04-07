import pulp as pl

v = [4, 2, 1, 10, 2]
w = [12, 2, 1, 4, 1]

x = pl.LpVariable.dicts('x', list(range(5)), cat='Binary')  # 5 binary variable

problem = pl.LpProblem('knapsack', pl.LpMaximize)  # a maximization problem called knapsack

# define target function
problem += x[0]*v[0] + x[1]*v[1] + x[2]*v[2] + x[3]*v[3] + x[4]*v[4]

# define constraints
problem += (
                x[0]*w[0] + x[1]*w[1] + x[2]*w[2] + x[3]*w[3] + x[4]*w[4] <= 15
            )

print(problem)

problem.solve()

print(f'Problem status: {pl.LpStatus[problem.status]}')
print(f'Optimal solution: We put the items {[i for i in range(5) if x[i].varValue==1]} into the knapsack.')
print(f'This solution achieves a value of ${pl.value(problem.objective)}.')
