from communication_cpp import CPP_SATSolver

class CPP_ImprovedBacktracker(CPP_SATSolver):
    def __init__(self, num_variables):
        super().__init__(num_variables, "cpp_executables\\improved_backtracker.exe")