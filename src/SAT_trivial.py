from itertools import product
from SAT import AbstractSATSolver,  SATClause

class TrivialSATSolver(AbstractSATSolver):
    def __init__(self, num_variables):
        super().__init__(num_variables)
    
    def initializeFromInput(self):
        raise NotImplementedError

    # returns an array of booleans containing a satisfying solution, or None if impossible
    def solve(self) -> list[int] | None:
        return self.trivial_solve()
    
    #checks wether a single clause is satisfied
    def check_clause_satisfaction(self, clause : SATClause, interpretation : list[bool]) -> bool:
        #checks wether at least one variable satisfies the clause
        variable_satisfaction = [interpretation[i] for i in clause.pos_variables]
        variable_satisfaction.extend([not interpretation[i] for i in clause.neg_variables])
        return any(variable_satisfaction)
    
    #checks wether all clauses satisfied
    def check_interpretation_satisfaction(self, interpretation : list[bool]) -> bool:
        clauses_satisfaction = [self.check_clause_satisfaction(clause, interpretation) for clause in self.clauses]
        return all(clauses_satisfaction)
    
    #trivial solving of sats. iterates over all interpretations.
    def trivial_solve(self) -> list[bool] | None:
        
        #finally, check all interpretations
        for interpretation in product([False, True], repeat = self.num_variables):
            if self.check_interpretation_satisfaction(interpretation):
                return list(interpretation)
        #if none found return None
        return None

