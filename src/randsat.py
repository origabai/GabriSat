from random import randint, sample
from SAT import DEFAULT_SOLVER

def generate_random(self, num_vars: int, num_clauses: int, solver = DEFAULT_SOLVER):
    s = solver(num_vars)
    forced_solution = [randint(0,1) for i in range(vars)]
    force_solvable: bool = (randint(0,1) == 0)
    for j in range(num_clauses):
        clause = sample([i for i in range(num_vars)], randint(1, num_vars-1))
        pos = []
        neg = []
        for x in clause:
            if (randint(0,1)==0):
                pos.append(x)
            else:
                neg.append(x)
        y = randint(0,num_vars-1)
        if (force_solvable):
            if (forced_solution[y]==0):
                neg.append(y)
            else:
                pos.append(y)
        s.addClause(pos, neg)
    return s