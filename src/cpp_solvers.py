from communication import CPP_SATSolver

class CPP_ImprovedBacktracker(CPP_SATSolver):
    def __init__(self, num_variables):
        super().__init__(num_variables, "ImprovedBacktrackingSolver")

class CPP_BacktrackingSolver_V2(CPP_SATSolver):
    def __init__(self, num_variables):
        super().__init__(num_variables, "BacktrackingSolver_V2")
    
class CPP_ThreadedSolver(CPP_SATSolver):
    def __init__(self, num_variables):
        super().__init__(num_variables, "ThreadedSolver")