from SAT import AbstractSATSolver

# abstract backtracking solver using the handler DS
class AbstractBacktrackingSolver(AbstractSATSolver):
    def __init__(self, num_variables, handler_ds):
        super().__init__(num_variables)
        self.handler_type = handler_ds
        self.clauses = []
    
    def solve(self) -> list[int] | None:
        self.handler = self.handler_type(self.num_variables,self.clauses)
        return self.rec_solve()

    def rec_solve(self) -> list[int] | None:
        curr_var = self.handler.next_var()
        # base case
        if (curr_var is None):
            return self.handler.current_assignment()
        
        # assign true
        self.handler.upd_assignment(curr_var, True)
        if (self.handler.valid()):
            sol = self.rec_solve()
            if sol is not None:
                return sol
        self.handler.rollback_assignment()

        # assign false
        self.handler.upd_assignment(curr_var, False)
        if (self.handler.valid()):
            sol = self.rec_solve()
            if sol is not None:
                return sol
        self.handler.rollback_assignment()

        return None
    
    def addClause(self, pos_variables: list[int], neg_variables: list[int]):
        self.clauses.append((pos_variables, neg_variables))
    