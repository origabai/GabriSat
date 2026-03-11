from random import randint, sample
from SAT import DEFAULT_SOLVER

"""
generates a random SAT of type solver, with num_vars and num_clauses
"""
def generate_random(num_vars: int, num_clauses: int, solver = DEFAULT_SOLVER):
    s = solver(num_vars)
    forced_solution = [randint(0,1) for i in range(num_vars)]
    # probability of 0.5 to force solvability
    force_solvable: bool = (randint(0,1) == 0)
    for j in range(num_clauses):
        # generates a random sample of variables, and assigns them randomly to neg and pos
        clause = sample([i for i in range(num_vars)], randint(1, num_vars-1))
        pos = []
        neg = []
        for x in clause:
            if (randint(0,1)==0):
                pos.append(x)
            else:
                neg.append(x)
        y = randint(0,num_vars-1)
        # force the clause to be satisfiable
        if (force_solvable):
            if (forced_solution[y]==0):
                neg.append(y)
            else:
                pos.append(y)
        s.addClause(pos, neg)
    return s