from itertools import product

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

    # returns an array of booleans containing a satisfying solution, or None if impossible
    def solve(self) -> list[int] | None:
        #TODO: add better solver
        return self.trivial_solve()
    
    
    
    
    
    
    #checks wether a single clause is satisfied
    def check_clause_satisfaction(self, clause : Clause, interpretation : list[bool]) -> bool:
            #checks wether at least one variable satisfies the clause
            variable_satisfaction = [interpretation[i] for i in clause.pos_variables]
            variable_satisfaction.extend([not interpretation[i] for i in clause.neg_variables])
            return any(variable_satisfaction)
    
    def check_interpretation_satisfaction(self, interpretation : list[bool]) -> bool:
        clauses_satisfaction = [self.check_clause_satisfaction(clause, interpretation) for clause in self.clauses]
        return all(clauses_satisfaction)
    
    #trivial solving of sats. iterates over all interpretations.
    def trivial_solve(self) -> list[bool] | None:
        
        #finally, check all interpretations
        for interpretation in product([False, True], repeat = self.num_variables):
            if self.check_interpretation_satisfaction(interpretation):
                return interpretation
        #if none found return None
        return None