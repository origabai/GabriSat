from communication import CPP_SATSolver, CPP_IDsolver

class CPP_ImprovedBacktracker(CPP_SATSolver):
    def __init__(self, num_variables):
        super().__init__(num_variables, "ImprovedBacktrackingSolver")

class CPP_BacktrackingSolver_V2(CPP_IDsolver):
    def __init__(self, num_variables):
        super().__init__(num_variables, "BacktrackingSolver_V2")
    
class CPP_ThreadedSolver(CPP_SATSolver):
    def __init__(self, num_variables):
        super().__init__(num_variables, "ThreadedSolver")
        
        
class CPP_BacktrackingSolver_V3(CPP_SATSolver):
    def __init__(self, num_variables):
        super().__init__(num_variables, "BacktrackingSolver_V3")


class CPP_IDsolverV3(CPP_IDsolver):
    def __init__(self, num_variables):
        super().__init__(num_variables, "BacktrackingSolver_V3")


class CPP_IDSudokuSolver(CPP_SATSolver):
    def __init__(self, num_variables):
        super().__init__(num_variables, "SudokuSolver")


class CPP_IDColoringSolver(CPP_IDsolver):
    def __init__(self, num_variables):
        print("AM I RU*NNING?")
        super().__init__(num_variables, "ColoringSolver")


class CPP_IDHamcycleSolver(CPP_SATSolver):
    def __init__(self, num_variables):
        super().__init__(num_variables, "HamcycleSolver")
