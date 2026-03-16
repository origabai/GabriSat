# an abstract data structure for handling SAT backtracking efficiently
class SATHandlingDS:
    def __init__(self, num_variables, clauses):
        self.num_variables = num_variables
        self.clauses = clauses

    # should return the next variable to be interpreted
    def next_var(self) -> int | None:
        pass

    # should return the current assignment of the variables
    def current_assignment(self) -> list[int]:
        pass
    
    # updates the assignment of a variable
    def upd_assignment(self, curr_var: int, value: bool):
        pass

    # rolls back the last variable assignment
    def rollback_assignment(self):
        pass

    # should return whether the current assignment has hope to be extended to a valid one
    def valid(self) -> bool:
        pass

    

