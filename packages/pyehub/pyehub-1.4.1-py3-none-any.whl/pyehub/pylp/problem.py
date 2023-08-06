"""
Contains functionality for dealing with a linear programming model.
"""
from typing import Iterable
from collections import namedtuple

import pulp
from contexttimer import Timer

from pylp.constraint import Constraint
import warnings


if pulp.__version__ == '2.1':
    import pulp.apis.core as solvers
    import pulp.apis.cplex_api as cplex
    import pulp.apis.glpk_api as glpk
else:
    import pulp.solvers as solvers
    warnings.warn('You are using pulp 2.0 or lower, pulp.apis.core has been changed to pulp.sovers automatically')

Status = namedtuple('Status', ['status', 'time'])


def solve(*, objective=None, constraints: Iterable[Constraint] = None,
          minimize: bool = False, solver: str = 'glpk',
          verbose: bool = False) -> Status:
    """
    Solve the linear programming problem.

    Args:
        objective: The objective function
        constraints: The collection of constraints
        minimize: True for minimizing; False for maximizing
        solver: The solver to use. Current supports 'glpk' and 'cplex'.
        verbose: If True, output the results of the solver

    Returns:
        A tuple of the status (eg: Optimal, Unbounded, etc.) and the elapsed
        time
    """
    if minimize:
        sense = pulp.LpMinimize
    else:
        sense = pulp.LpMaximize

    problem = pulp.LpProblem(sense=sense)

    # Objective function is added first
    problem += objective.construct()

    if constraints:
        for constraint in constraints:
            problem += constraint.construct()

    if solver == 'glpk' and pulp.__version__ == '2.1':
        solver = glpk.GLPK_CMD(msg=verbose)
    elif solver == 'glpk' and pulp.__version__ != '2.1':
        solver = solvers.GLPK(msg=verbose)
    elif solver == 'cplex' and pulp.__version__ == '2.1':
        solver = cplex.CPLEX_CMD(msg=verbose)
    elif solver == 'cplex' and pulp.__version__ != '2.1':
        solver = solvers.CPLEX(msg=verbose)
    else:
        raise ValueError(f'Unsupported solver: {solver}')

    with Timer() as time:
        results = problem.solve(solver)

    status = pulp.LpStatus[results]

    return Status(status=status, time=time.elapsed)
