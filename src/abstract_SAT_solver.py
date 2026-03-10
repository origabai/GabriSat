"""
an abstract interface for a SAT problem.
all classes implementing SAT-solvers should inherit this one.
"""
class SATClause:
    def __init__(self, pos_variables, neg_variables):
        self.pos_variables = pos_variables
        self.neg_variables = neg_variables

class AbstractSATSolver:
    def __init__(self, num_variables):
        self.num_variables = num_variables
        self.clauses = []

    def addClause(self, pos_variables: list[int], neg_variables: list[int]):
        self.clauses.append(SATClause(pos_variables, neg_variables))

    # if you inherit you should implement this function.
    # it should return a solution if one exists, and None otherwise
    def solve(self) -> list[int] | None:
        pass