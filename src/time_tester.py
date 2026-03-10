from SAT_reducible_problem import SATReducibleProblem
from time import time

# run problem of size problem_size for some number of trials, and average the execution times
def test_time(problem: SATReducibleProblem, problem_size: int, trials = 5):
    sm = 0
    for _ in range(trials):
        problem = problem.generate(problem_size)
        start = time()
        problem.solve()
        end = time()
        sm += end - start
    return sm / trials