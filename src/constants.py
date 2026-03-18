from SAT_trivial import TrivialSATSolver
from trivial_backtracker import TrivialBacktrackingSolver
from improved_backtracking import ImproverBacktrackingSolver
from cpp_solvers import CPP_ImprovedBacktracker

DEFAULT_SOLVER = CPP_ImprovedBacktracker
TrivialSATSolver
TrivialBacktrackingSolver
ImproverBacktrackingSolver
CPP_ImprovedBacktracker

RandomGraphMinSize = 5
RandomGraphMaxSize = 13

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

CLEAR_LABEL = {'display': 'none'}
LABEL = {'display': 'none'}
CLEAR_SELECTOR = {'display': 'none', 'width': '300px', 'marginTop': '5px'}
SELECTOR = {'display': 'block', 'width': '300px', 'marginTop': '5px'}