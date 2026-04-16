from SAT_reducible_problem import SATReducibleProblem
from constants import DEFAULT_SOLVER
from time import time

# run problem of size problem_size for some number of trials, and average the execution times
def test_time(problem: SATReducibleProblem, problem_size: int, trials = 10, satsolver = DEFAULT_SOLVER):
    sm = 0
    for _ in range(trials):
        problem = problem.generate(problem_size, satsolver)
        start = time()
        problem.solve()
        end = time()
        sm += end - start
    return sm / trials