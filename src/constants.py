from SAT_trivial import TrivialSATSolver
from trivial_backtracker import TrivialBacktrackingSolver
from improved_backtracking import ImproverBacktrackingSolver
from cpp_solvers import CPP_ImprovedBacktracker, CPP_BacktrackingSolver_V2, CPP_BacktrackingSolver_V3, CPP_IDsolver

DEFAULT_SOLVER = CPP_IDsolver
TrivialSATSolver
TrivialBacktrackingSolver
ImproverBacktrackingSolver
CPP_ImprovedBacktracker
CPP_BacktrackingSolver_V2
CPP_BacktrackingSolver_V3
CPP_IDsolver

SUDOKU_GEN_STATUS = "NEW_seed" #can be NEW_seed, NEW, OLD, NEW_VARIABLE
SUDOKU_GEN_LIMIT = 3

SYMMETRY_TOGGLE = True
MAX_SYMMETRY_OPERATIONS = 1000000 #lets say a million

RandomGraphMinSize = 5
RandomGraphMaxSize = 13
HAMCYCLE_GENERATION_CONST = 8

SudokuBoxMiddle = [400, 250] # half of the graph box size
SudokuCircleConstant = 18

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