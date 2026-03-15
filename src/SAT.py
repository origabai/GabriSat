from random import randint, sample
"""
an abstract interface for a SAT problem.
all classes implementing SAT-solvers should inherit this one.
"""


class SATClause:
    def __init__(self, pos_variables: set[int], neg_variables: set[int]):
        self.pos_variables: set[int] = pos_variables
        self.neg_variables: set[int] = neg_variables

    def size(self):
        return len(self.pos_variables) + len(self.neg_variables)

class AbstractSATSolver:
    def __init__(self, num_variables):
        self.num_variables = num_variables
        self.clauses: list[SATClause] = []

    def addClause(self, pos_variables: list[int], neg_variables: list[int]):
        self.clauses.append(SATClause(set(pos_variables), set(neg_variables)))

    # if you inherit you should implement this function.
    # it should return a solution if one exists, and None otherwise
    def solve(self) -> list[int] | None:
        pass

    
    """
    generates a random SAT of type solver, with num_vars and num_clauses
    """
    @classmethod
    def generate_random(self, num_vars: int, num_clauses: int, solver):
        s = solver(num_vars)
        forced_solution = [randint(0, 1) for i in range(num_vars)]
        # probability of 0.5 to force solvability
        force_solvable: bool = randint(0, 1) == 0
        for j in range(num_clauses):
            # generates a random sample of variables, and assigns them randomly to neg and pos
            clause = sample([i for i in range(num_vars)], randint(1, num_vars - 1))
            pos = []
            neg = []
            for x in clause:
                if randint(0, 1) == 0:
                    pos.append(x)
                else:
                    neg.append(x)
            y = randint(0, num_vars - 1)
            # force the clause to be satisfiable
            if force_solvable:
                if forced_solution[y] == 0:
                    neg.append(y)
                else:
                    pos.append(y)
            s.addClause(pos, neg)
        return s
