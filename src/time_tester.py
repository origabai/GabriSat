from SAT_reducible_problem import SATReducibleProblem
from constants import DEFAULT_SOLVER
from time import time, sleep
from copy import deepcopy
import signal
from contextlib import contextmanager
import os

class TimeoutException(Exception): pass


# run problem of size problem_size for some number of trials, and average the execution times
def test_time(problem: SATReducibleProblem, problem_size: int, trials = 30, satsolver = DEFAULT_SOLVER):
    sm = 0
    print("generating size", problem_size)
    problem = problem.generate(problem_size, satsolver)
    problems = [deepcopy(problem) for i in range(trials)]
    times = []
    for i in range(trials):
        #problem = problem.generate(problem_size, satsolver)
        start = time()
        
        pid = os.fork()
        if pid:
            sleep(5)
            os.kill(pid, signal.SIGSTOP)
        else:
            problems[i].solve()
            print("CYBER!!!!!!!!!!")
            end = time()
            dt = end - start
            print(dt)
            exit()
            
        end = time()
        dt = end - start
        print(dt)
        sm += end - start
    #print(times)
    return sm / trials