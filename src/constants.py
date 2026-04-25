from SAT_trivial import TrivialSATSolver
from trivial_backtracker import TrivialBacktrackingSolver
from improved_backtracking import ImproverBacktrackingSolver
from cpp_solvers import CPP_ImprovedBacktracker, CPP_BacktrackingSolver_V2

DEFAULT_SOLVER = CPP_BacktrackingSolver_V2
TrivialSATSolver
TrivialBacktrackingSolver
ImproverBacktrackingSolver
CPP_ImprovedBacktracker
CPP_BacktrackingSolver_V2

SUDOKU_GEN_STATUS = "NEW_VARIABLE" #can be NEW_seed, NEW, OLD, NEW_VARIABLE
SUDOKU_GEN_LIMIT = 3

RandomGraphMinSize = 5
RandomGraphMaxSize = 13
HAMCYCLE_GENERATION_CONST = 8

ColourSelectorOptions = [
                        # 'label' is what the user sees, 'value' is what Python receives
                        {'label': 'None (none selected)', 'value': None},
                        {'label': 'grey (no colour)', 'value': 'grey'},
                        {'label': 'red (0)', 'value': 'red'},
                        {'label': 'green (1)', 'value': 'green'},
                        {'label': 'blue (2)', 'value': 'blue'},
                        {'label': 'yellow (3)', 'value': 'yellow'},
                        {'label': 'purple (4)', 'value': 'purple'},
                        {'label': 'pink (5)', 'value': 'pink'},
                        {'label': 'magenta (6)', 'value': 'magenta'},
                        {'label': 'lime (7)', 'value': 'lime'},
                        {'label': 'cyan (8)', 'value': 'cyan'},
                    ]