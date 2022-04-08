from typing import List, Tuple
import itertools
import numpy as np
import pulp as pl

T = 20
P = 3


def leftright(x: List[int]) -> Tuple[str, str]:
    """Takes a list of three strings and returns two strings encoding the position
       of wolf, goat and kabbage."""
    codes = ('w', 'g', 'k')
    left_river_bank = ''.join([codes[i] for i in range(len(codes)) if x[i] == 1])
    right_river_bank = ''.join([codes[i] for i in range(len(codes)) if x[i] == 0])
    return left_river_bank, right_river_bank


if __name__ == '__main__':
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
        for passenger in range(3):
            if t % 2 == 0:  # only allowed to cross river from original to target bank in even time steps
                problem += (
                             x[(t + 1, passenger)] - x[(t, passenger)] <= 0
                           )
            else:  # only allowed to cross river from target back to original bank in odd time steps
                problem += (
                             x[(t + 1, passenger)] - x[(t, passenger)] >= 0
                           )
        # at most one passenger is allowed to cross the river in each time step
        sign = -1 if t % 2 == 0 else 1
        problem += (
                    sign * (x[(t + 1, 0)] - x[(t, 0)]) +
                    sign * (x[(t + 1, 1)] - x[(t, 1)]) +
                    sign * (x[(t + 1, 2)] - x[(t, 2)]) <= 1
                   )

        # nobody gets eaten
        if t % 2 == 0:
            # at most one of wolf and goat on target river bank
            # x[t, 2] on the left hand side allows that everybody's on the target bank
            problem += (
                        x[t, 2] <= x[t, 0] + x[t, 1]
                       )
            # at most one of goat and kabbage on target river bank
            # x[t, 0] on the left hand side allows that everybody's on the target bank
            problem += (
                        x[t, 0] <= x[t, 1] + x[t, 2]
                       )
        else:
            # at most one of wolf and goat on original river bank
            problem += (
                         x[t, 0] + x[t, 1] <= 1
                       )
            # at most one of goat and kabbage on original river bank
            problem += (
                         x[t, 1] + x[t, 2] <= 1
                       )

    print(problem)

    problem.solve()

    print(f'Problem status: {pl.LpStatus[problem.status]}')

    # bring solution values into a less clumsy format, with sol[t][i] = x[(t, i)].varValue
    sol = [[x[(t, 0)].varValue, x[(t, 1)].varValue, x[(t, 2)].varValue] for t in range(T)]
    min_boat_crossings = min([t for t in range(T) if sol[t][0] == 0 and sol[t][1] == 0 and sol[t][2] == 0])

    print()
    for t in range(min_boat_crossings+1):
        left_bank, right_bank = leftright(sol[t])
        boat = 'b      ' if t % 2 == 0 else '      b'
        print(f'Step {t:02d}:   {left_bank:>3}  |{boat}|  {right_bank}')

    print()
    print(f'This solution solves the problem in after the boat has crossed the river {min_boat_crossings} times.')
    print(f'It achieves a target function value of {pl.value(problem.objective)}.')
