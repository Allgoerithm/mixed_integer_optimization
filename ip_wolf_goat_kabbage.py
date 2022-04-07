import itertools
import numpy as np
import pulp as pl

T = 20
P = 3

# possible index values: 20 timesteps plus 3 passengers (0= wolf, 1=goat, 2=cabbage)
indexes = list(itertools.product(range(T), range(P)))

# x[(0, 0)] = 1 means that the wolf is on the original river bank in time step 0
x = pl.LpVariable.dicts(name='x', indices=indexes, cat='Binary')

# define problem
problem = pl.LpProblem('wolf_goat_kabbage', pl.LpMinimize)

target = 0
# define target function
for t in range(T):
    for p in range(P):
        target += np.power(P+1, t) * x[(t, p)]

problem += target

# define constraints

# everybody is on the original river bank at the beginning (t==0)
problem += x[(0, 0)] == 1
problem += x[(0, 1)] == 1
problem += x[(0, 2)] == 1

# only one passenger is allowed for each river crossing
for t in range(T-1):
    for signs in list(itertools.product([-1, 1], [-1, 1], [-1, 1])):
        problem += (
                    signs[0] * (x[(t, 0)] - x[(t + 1, 0)]) +
                    signs[1] * (x[(t, 1)] - x[(t + 1, 1)]) +
                    signs[2] * (x[(t, 2)] - x[(t + 1, 2)]) <= 1
                   )

# for all even time steps (boat on the original river bank), nobody gets eaten on the target river bank
#

print(problem)

problem.solve()

print(f'Problem status: {pl.LpStatus[problem.status]}')

for t in range(T):
    print(f'{x[(t, 0)].varValue}, {x[(t, 1)].varValue}, {x[(t, 2)].varValue}')

print(f'This solution achieves a value of {pl.value(problem.objective)}.')


