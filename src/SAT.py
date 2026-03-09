from typing import Generator, NewType

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
    
    #Add new clause
    def addClause(self, pos_variables, neg_variables):
        self.clauses.append(self.Clause(pos_variables, neg_variables))

    # returns an array of booleans containing a satisfying solution, or None if unsat
    def solve(self):
        #TODO: add better solver
        return self.trivial_solve()
    
    #trivial solving of sats. iterates over all interpretations.
    def trivial_solve(self) -> list[bool]:
            
        #iterates over all possible interpretations
        def interpretation_iterator(num_variables : int) -> Generator[list[bool]]:
            #initial zero interpretation
            interpretation = [False]*num_variables
            
            #get next interpretation
            def get_next_interpretation(interpretation : list[bool]) -> list[bool] | None:
                # if zero not in interpretation, it is the last one.
                if False not in interpretation:
                    return None
                
                #find first zero in interpretation
                first_false_position = interpretation.index(False)
                
                #construct next interpretation 
                next_interpretation = [False] * first_false_position
                next_interpretation.append(True)
                next_interpretation.extend(interpretation[first_false_position + 1:])
                return next_interpretation
            
            #yields interpretations
            while interpretation:
                yield interpretation
                interpretation = get_next_interpretation(interpretation)
        
        #checks wether all clauses are satisfied
        #Adding new type bcs pylance doens't like static types >:[
        Clause = NewType('Clause', self.Clause) 
        def check_interpretation_satisfaction(clauses : list[Clause], interpretation : list[bool]):
            #checks wether a single clause is satisfied
            def check_clause_satisfaction(clause : Clause, interpretation : list[bool]):
                #checks wether at least one variable satisfies the clause
                variable_satisfaction = [interpretation[i] for i in clause.pos_variables]
                variable_satisfaction.extend([not interpretation[i] for i in clause.neg_variables])
                return any(variable_satisfaction)
            
            #check and return all clause satisfaction
            clauses_satisfaction = [check_clause_satisfaction(clause, interpretation) for clause in clauses]
            return all(clauses_satisfaction)
        
        #finally, check all interpretations
        for interpretation in interpretation_iterator(self.num_variables):
            if check_interpretation_satisfaction(self.clauses, interpretation):
                return interpretation
        #if none found return None
        return None