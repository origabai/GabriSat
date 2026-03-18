from communication import CPP_SATSolver

class CPP_ImprovedBacktracker(CPP_SATSolver):
    def __init__(self, num_variables):
        super().__init__(num_variables, "ImprovedBacktrackingSolver")