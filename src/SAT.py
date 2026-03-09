"""
SAT problem
"""
class SAT:
    class Clause:
        def __init__(self, pos_variables, neg_variables):
            self.pos_variables = pos_variables
            self.neg_variables = neg_variables


    def __init__(self, num_variables):
        self.num_variables = num_variables
        self.clauses = []
    
    def initializeFromInput(self):
        pass

    def addClause(self, pos_variables, neg_variables):
        self.clauses.append(self.Clause(pos_variables, neg_variables))

    # returns an array of booleans containing a satisfying solution, or None if unsat
    def solve(self):
        pass

