from abstract_SAT_solver import AbstractSATSolver

class TrivialBacktrackingSolver(AbstractSATSolver):
    def __init__(self, num_variables):
        super().__init__(num_variables)

    # returns an array of booleans containing a satisfying solution, or None if impossible
    def solve(self) -> list[int] | None:
        self.curr_interp = [None for i in range(self.num_variables)]
        return self.solve_backtrack(0)

    # checks whether the current interpretation can be reasonably extended(no immediate problems)
    def check_curr_interp(self):
        # check whether every clause can be extended
        for c in self.clauses:
            val = False
            for p in c.pos_variables:
                if (self.curr_interp[p] is None):
                    val = True
                    break
                else:
                    val |= self.curr_interp[p]
            for p in c.neg_variables:
                if (self.curr_interp[p] is None):
                    val = True
                    break
                else:
                    val |= not self.curr_interp[p]
            # if the clause is alreafy unsatistified
            if (not val):
                return False
        return True

    # helper function for solve
    def solve_backtrack(self, ind: int):
        if (ind == self.num_variables):
            return self.curr_interp
        # go over all options for interpretations
        self.curr_interp[ind] = False
        if self.check_curr_interp():
            sol = self.solve_backtrack(ind+1)
            if sol is not None:
                return sol
        self.curr_interp[ind] = True
        if self.check_curr_interp():
            sol = self.solve_backtrack(ind+1)
            if sol is not None:
                return sol
        self.curr_interp[ind] = None
        return None

        
