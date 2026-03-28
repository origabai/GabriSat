from dash import Dash, html, Input, Output, State, dcc, ctx, no_update
from dash.exceptions import PreventUpdate
import dash_cytoscape as cyto
import _thread
from random import randint
from graph_coloring import GraphColoring
from sudoku import Sudoku
from hamiltonian_cycle import HamiltonianCycle
from constants import RandomGraphMinSize, RandomGraphMaxSize, ColourSelectorOptions
from UI_layout import UILayout
from uuid import uuid4


"""
provides utils for visualizer.py
"""


class UIUtils:
    """
    here are all of the functions that the UI uses.
    """

    def __init__(self, app: Dash, vis_object):
        self.vis_object = vis_object
        self.app = app
        self.layout = UILayout(self).default_layout

    """
    generates initial graph element data. makes them accordingly to self.
    """

    def generate_initial_graph_data(self, special_edges=[], missing_nodes=[]):
        # handle zero input
        graph = self.vis_object.graph

        # print("MISSING NODES ARE: ", missing_nodes)
        initial_data = []
        # generates nodes in initial_data
        for node in range(graph.num_nodes):
            if node not in missing_nodes:
                initial_data.append(
                    {
                        "data": {
                            "id": str(node),
                            "label": str(node),
                            "color": self.vis_object.get_color_at_node(node),
                        }
                    }
                )

        # adds edges -  special edges are a list of edges to colour green. long if statement for undigraph support
        for edge in graph.edges:
            initial_data.append(
                {
                    "data": {
                        "source": str(edge[0]),
                        "target": str(edge[1]),
                        "color": "grey",
                    }
                }
            )
            if edge in special_edges or [edge[1], edge[0]] in special_edges:
                initial_data[-1]["data"]["color"] = "ForestGreen"

        # exits
        return initial_data

    """
    handles press of "add node" button.
    """

    def add_node(self, n_clicks, current_elements):
        # finds existing nodes
        current_nodes = [
            int(element["data"]["id"])
            for element in current_elements
            if "target" not in element["data"]
        ]
        # finds next node to add
        next_id = min(set(range(0, len(current_nodes) + 2)) - set(current_nodes))
        # Construct the new node dictionary and append it to the state
        new_node = {
            "data": {"id": str(next_id), "label": str(next_id), "color": "grey"}
        }
        current_elements.append(new_node)

        return current_elements

    # TODO: replace with better add edge capabilities.
    """
    currently handles edge addition. TEMPORARY!
    """

    def add_edge(self, n_clicks, source_id, target_id, current_elements):
        source_id = str(source_id)
        target_id = str(target_id)
        node_ids = [
            element["data"]["id"]
            for element in current_elements
            if self.is_node(element)
        ]
        if (
            not source_id
            or not target_id
            or source_id not in node_ids
            or target_id not in node_ids
            or source_id == target_id
        ):
            return current_elements, "Invalid input!", {"color": "red"}
            # Do nothing if source/target are empty or not real, or self edge

        # Construct the new edge dictionary and append it to the state
        new_edge = {"data": {"source": source_id, "target": target_id, "color": "grey"}}
        if all(
            not self.are_edges_equal(new_edge, element) for element in current_elements
        ):
            current_elements.append(new_edge)
        else:
            return current_elements, "Edge already exists!", {"color": "red"}

        return current_elements, "Edge added successfully!", {"color": "green"}

    """
    returns true iff edge1 and edge 2 are equivalent up to order, id and color
    """

    def are_edges_equal(self, edge1, edge2) -> bool:
        if not self.is_edge(edge1) or not self.is_edge(edge2):
            return False
        nodes1: set = {edge1["data"]["source"], edge1["data"]["target"]}
        nodes2: set = {edge2["data"]["source"], edge2["data"]["target"]}
        # set representing the nodes of the edges
        return nodes1 == nodes2

    """
    handles press of erase button.
    """

    def switch_erasing_mode(self, n_clicks):
        if n_clicks % 2 == 0:
            return {"toggled": False}, {
                "backgroundColor": "lightgray",
                "color": "black",
                "padding": "10px",
            }
        else:
            return {"toggled": True}, {
                "backgroundColor": "red",
                "color": "black",
                "padding": "10px",
            }

    """
    checks wether an element is an edge.
    """

    def is_edge(self, element):
        return "target" in element["data"]

    """
    checks wether an element is adjacent to a certain node.
    returns true if this is the node itself or an adjacent edge.
    """

    def is_adjacent_to(self, edge, node_id):
        if edge["data"]["id"] == node_id:
            return True
        if not self.is_edge(edge):
            return False
        return node_id in [edge["data"]["target"], edge["data"]["source"]]

    # returns true if an element is a node
    """
    checks if a ui element is a node.
    """

    def is_node(self, element):
        return not self.is_edge(element)

    """
    colors all element grey, with respect to variable criterion function
    """

    def color_to_grey(self, elements, criterion):
        new_elements = []
        for element in elements:
            new_elements.append(element)
            if criterion(element):
                new_elements[-1]["data"]["color"] = "grey"
        return new_elements

    # checks if an element is of a colour aligning with the selected one - if larger, returns false.
    """
    checks if an element's color is aligned with the current restrictions.
    """

    def check_element_color_compliance(self, element, color):
        if (
            element["data"]["color"] == "grey"
            or element["data"]["color"] == "ForestGreen"
        ):
            return False

        return 1 + self.vis_object.color_to_num(element["data"]["color"]) > int(color)

    """
    handles change of color number
    """

    def handle_color_num_change(self, value, current_elements):
        # options for colour selector - depending on colour.
        next_options = ColourSelectorOptions[: int(value) + 2]

        # changes up the values of all nodes
        def compare_color(element):
            return self.check_element_color_compliance(element, value)

        new_elements = self.color_to_grey(current_elements, compare_color)
        # also changes the settings of the options
        return next_options, new_elements

    """
    removes edges adjacent to a node (and the node itself)
    """

    def remove_adjacent_edges(self, tapped_node_id, elements):
        return [
            element
            for element in elements
            if not self.is_adjacent_to(element, tapped_node_id)
        ]

    """
    recolors node
    """

    def recolor_node(self, elements, color, node_id):
        elements = [element for element in elements if element["data"]["id"] != node_id]
        elements.append({"data": {"id": node_id, "label": node_id, "color": color}})
        return elements

    """
    processes node click. currently can remove a node, or color it.
    """

    def process_node_click(
        self,
        tapped_node,
        current_elements,
        selected_colour,
        erase_mode,
        max_num,
        current_mode,
    ):
        # Base case: The app just loaded, and no node has been clicked yet.
        if tapped_node is None:
            return current_elements

        # if erasing:
        if erase_mode["toggled"]:
            return self.remove_adjacent_edges(tapped_node["id"], current_elements)
        else:
            # check need to color depending on selected color
            trivial_conditions = current_mode != "COLOR" or selected_colour is None
            if (
                trivial_conditions
                or self.vis_object.color_to_num(selected_colour) > int(max_num) - 1
            ):
                return current_elements
            # now, recolor when needed:
            return self.recolor_node(
                current_elements, selected_colour, tapped_node["id"]
            )

    """
    generates random graph - returns elements accordingly and updates graph in self.
    """

    def generate_random_graph(self, n_clicks, current_elements, size):
        # handles automatic activation at creation
        if n_clicks == 0:
            return current_elements
        # bad size input
        if not size: # make it random
            size = randint(RandomGraphMinSize, RandomGraphMaxSize)
        # making size an int fitting in the legal range
        size = int(size)
        size = max(size, RandomGraphMinSize)
        size = min(size, RandomGraphMaxSize)
        # generates and updates new graph
        self.vis_object.graph = GraphColoring.generate(num_of_nodes=size)
        return self.generate_initial_graph_data(missing_nodes=[])

    """
    function that checks wether edge is connecting between id1 and id2.
    """

    def is_edge_connecting(self, edge, id1, id2):
        if not self.is_edge(edge):
            return False
        else:
            edge_bounds = set([edge["data"]["source"], edge["data"]["target"]])
            return edge_bounds == set([id1, id2])

    def erase_edge(self, elements, id1, id2):
        return [
            element
            for element in elements
            if not self.is_edge_connecting(element, id1, id2)
        ]

    """
    function that is responsible for edge clicks. currently removes it if needed.
    """

    def process_edge_click(self, tapped_edge, current_elements, erase_mode):
        # remove edge if necessary
        if tapped_edge is not None and erase_mode["toggled"]:
            return self.erase_edge(
                current_elements, tapped_edge["source"], tapped_edge["target"]
            )
        # base case - dont respond if un-needed
        return current_elements

    """
    takes a UI graph elemnt and returns it's color in graph readable format.
    """

    def parse_color_for_graph(self, element):
        value = self.vis_object.color_to_num(element["data"]["color"])

        if value == -1:
            return None
        return value

    """
    goes over graph data in UI and returns it in parsed form for later use
    """

    def parse_current_graph_data(self, elements):
        nodes = []
        node_color_array = []
        edges = []

        for element in elements:
            if self.is_node(element):
                new_id = int(element["data"]["id"])
                nodes.append(new_id)
                new_color = self.parse_color_for_graph(element)
                node_color_array.append([new_id, new_color])

            elif self.is_edge(element):
                edges.append(
                    [int(element["data"]["source"]), int(element["data"]["target"])]
                )

        return nodes, edges, node_color_array

    """
    useful for searching fro color - if not present returns -1.
    """

    def smart_index(self, array, index):
        try:
            return array.index(index)
        except ValueError:
            return -1

    """
    reduces elements and indices to match current graph standard.
    """

    def reduce_excess_nodes(self, nodes, edges, color_tuples):
        # check for empty case
        if nodes == []:
            return [], [], [], []

        nodes.sort()
        original_nodes = nodes
        new_value = [self.smart_index(nodes, num) for num in range(max(nodes) + 1)]

        # reduce nodes
        nodes = [new_value[node] for node in nodes]

        # reduce edges
        edges = [[new_value[edge[0]], new_value[edge[1]]] for edge in edges]

        # reduce color tuples:
        color_tuples = [[new_value[tup[0]], tup[1]] for tup in color_tuples]

        # return reduced
        return nodes, edges, color_tuples, original_nodes

    """
    constructs a graph from parsed elements
    """

    def construct_new_graph(self, nodes, edges, color_tuples, max_colors):
        color_tuples.sort(key=lambda tup: tup[0])
        color_array = [element[1] for element in color_tuples]
        return GraphColoring(len(nodes), edges, color_array, max_colors)

    """
    constructs graph from elements in ui. reduces indices accordingly.
    returns graph as well as original nodes for oxidation.
    """

    def construct_graph_from_elements(self, elements, max_colors):
        new_nodes, new_edges, new_color_tuples = self.parse_current_graph_data(elements)
        new_nodes, new_edges, new_color_tuples, original_nodes = (
            self.reduce_excess_nodes(new_nodes, new_edges, new_color_tuples)
        )
        return original_nodes, self.construct_new_graph(
            new_nodes, new_edges, new_color_tuples, max_colors
        )

    """
    solves color problem on self.vis_object_graph
    """

    def generate_solved_colors(self):
        solution = self.vis_object.graph.solve()
        if solution is None:
            solution = [None] * self.vis_object.graph.num_nodes

        return solution != [None] * self.vis_object.graph.num_nodes, solution

    """
    generates hamiltonian path of self.vis_object.graph
    """

    def generate_solved_hampath(self):
        ham_graph = HamiltonianCycle(
            self.vis_object.graph.num_nodes, self.vis_object.graph.edges
        )
        ham_solution = ham_graph.solve()

        return ham_solution is not None, self.vis_object.generate_edges(ham_solution)

    """
    helper function. resolves the problem on self.vis_object.graph. also raises back node indices
    """

    def solve_problems(self, problem, original_nodes):
        new_colors = self.vis_object.graph.colors
        hampath_edges = []

        if problem == "COLOR":
            found_solution, found_colors = self.generate_solved_colors()
            if found_solution:
                new_colors = found_colors
        elif problem == "HAMPATH":
            found_solution, hampath_edges = self.generate_solved_hampath()
        else:
            found_solution = False

        self.vis_object.graph.colors = new_colors
        # raise nodes back up after solving
        hampath_edges, missing_nodes = self.oxidize_graph(original_nodes, hampath_edges)
        new_graph_data = self.generate_initial_graph_data(hampath_edges, missing_nodes)
        return found_solution, new_graph_data

    """
    does the inverse of the reduce graph function. returns an array of missing nodes. also reduces ham_edges
    """

    def oxidize_graph(self, original_nodes, ham_edges):
        if original_nodes == []:
            return [], set([])

        # useful for algorithmics later
        original_nodes.sort()

        # updating curreng graph parameters
        self.vis_object.graph.num_nodes = max(original_nodes) + 1
        self.vis_object.graph.edges = [
            [original_nodes[edge[0]], original_nodes[edge[1]]]
            for edge in self.vis_object.graph.edges
        ]
        ham_edges_reduced = [
            [original_nodes[edge[0]], original_nodes[edge[1]]] for edge in ham_edges
        ]

        # updating graph colors
        new_colors = [-1] * (max(original_nodes) + 1)
        for ind in range(len(self.vis_object.graph.colors)):
            new_colors[original_nodes[ind]] = self.vis_object.graph.colors[ind]
        self.vis_object.graph.colors = new_colors

        # return set of missing nodes
        return ham_edges_reduced, set(range(0, max(original_nodes))) - set(
            original_nodes
        )

    """
    processes press of "do action" button. takes in state input and returns output message and new graph components.
    besides that, updates the graph with reduced elements.
    """

    def do_task(self, n_clicks, elements, max_colors, problem, sudoku_board, size_of_sudoku):
        message: str # success message to return
        color: dict # color of message
        # prevent accidental press.
        if n_clicks == 0:
            print("i have no clue how to fix this, thats a bug.")
            return "this is unusual...", {"color": "yellow"}, no_update, no_update

        # handle end program:
        if problem == "END":
            self.vis_object.correct_end = True
            _thread.interrupt_main()
            return "The program finished running. ", {"color": "blue"}, no_update, no_update
        
        if problem in ["COLOR", "HAMPATH"]:

            # now, for the interesting case:
            original_nodes, self.vis_object.graph = self.construct_graph_from_elements(
                elements, int(max_colors)
            )
            found_solution, elements = self.solve_problems(problem, original_nodes)

            if found_solution:
                message = "Everything good, proceed!"
                color = {"color": "green"}
            else:
                message = "No solution found!"
                color = {"color": "red"}
        
        if problem == "SUDOKU":
            # making a backend_board
            board = self.sudoku_frontend_to_backend(sudoku_board, int(size_of_sudoku))
            sudoku = Sudoku(board)
            solution = sudoku.solve() # backend solving
            if solution is None: # no solution
                message = "No solution found!"
                color = {"color": "red"}
            else: # solution found
                message = "Everything good, proceed!"
                color = {"color": "green"}
                # reassembling the frontend board
                sudoku_board = self.sudoku_backend_to_frontend(sudoku_board, solution)
        return message, color, elements, sudoku_board
    
    """
    called when the task selector is changed, switches what is shown on screen to match the new task
    """
    def switch_problem(self, problem, graph_style, sudoku_style, coloring_style, current_elements):
        message: str # message to display to user
        color: dict # color of message
        # first hide everything
        graph_style['display'] = 'none'
        sudoku_style['display'] = 'none'
        coloring_style['display'] = 'none'
        if problem == "HAMPATH":
            graph_style['display'] = 'block' # show graph div
            message = "Finding a hamiltonian cycle"
            color = {'color' : 'black'}
            # returns cleared out nodes and hides color parts
            current_elements = self.color_to_grey(current_elements, self.is_node)
        if problem == "COLOR":
            graph_style['display'] = 'block' # show graph div
            coloring_style['display'] = 'block' # within graph div show elements for coloring
            message = "Finding a coloring"
            color = {'color' : 'black'}
            # when switching to color we need to clear out all coloured edges
            current_elements = self.color_to_grey(current_elements, self.is_edge)
        if problem == "SUDOKU":
            sudoku_style['display'] = 'block' # show sudoku div
            message = "Solving a sudoku"
            color = {'color' : 'black'}
        if problem == "END":
            message = "Leaving? :("
            # don't show anything
            color = {'color' : 'black'}
        return message, color, graph_style, sudoku_style, coloring_style, current_elements
    
    """
    creates html elements of an empty sudoku board of size x size, initialized with board
    if board is None it initializes empty
    """
    def create_sudoku_board(self, size: int, given_board: list[list[int| None]] | None = None):
        version = str(uuid4()) # unique id, fixes a memory bug
        square_size: int = int(size ** .5) # size of sudoku squares
        board = [] # list of the cells
        for row in range(size):
            for column in range(size):
                cell_style = { # creating the style for the cell
                        "fontSize": f"{27 / size}rem", 
                        "fontWeight": "bold",
                        "aspect ratio": "1 / 1",
                        "font size": "{1px}",
                        "borderTop": "1px solid #ccc", # thin gray border
                        "borderLeft": "1px solid #ccc",
                        "borderBottom": "1px solid #ccc",
                        "borderRight": "1px solid #ccc",
                        "backgroundColor": "white",
                        "margin": "0",
                        "padding": "0",
                        "color": "black",
                }
                # making the borders of the squares
                if row % square_size == 0: # first of the row
                        cell_style["borderTop"] = "2px solid black"
                if (row + 1) % square_size == 0: # last of the row
                        cell_style["borderBottom"] = "2px solid black"
                if column % square_size == 0: # first of the column
                        cell_style["borderLeft"] = "2px solid black"
                if (column + 1) % square_size == 0: # last of the column
                        cell_style["borderRight"] = "2px solid black"
                cell_text: str = "" # default empty text
                if given_board is not None and given_board[row][column] is not None:
                    cell_text = str(given_board[row][column] + 1)
                cell = html.Button(
                    cell_text,
                    id={'type' : 'sudoku-cell', 'row' : row, 'col' : column, 'version': version},
                    style=cell_style,
                )
                board.append(cell)

        return board
    
    """
    called when the sudoku size selector is changed
    """
    def change_sudoku_size(self, size, board_div, board_children, board_style, board_key):
        message: str # message to display to user
        color: dict # color of message
        if size == "0": # hide board
            board_div['display'] = 'none'
            message = "Please choose a board size!"
            color = {'color': 'black'}
        else: # construct board
            board_div['display'] = 'block'
            message = f"Sudoku board of size {size}x{size}"
            color = {'color': 'black'}
            pixel_size=576 # a good size, and divisible by 4, 9 and 16
            board_children = self.create_sudoku_board(int(size)) # creating the actual board
            board_style = {
                        'display': 'grid',
                        'gridTemplateColumns': f'repeat({size}, 1fr)', 
                        'gridTemplateRows': f'repeat({size}, 1fr)',
                        'width': f'{pixel_size}px',
                        'height': f'{pixel_size}px',
                        'border': '3px solid black',
                        'marginTop': '20px',
                        'gap': '0px',
                    }
            # a unique key for different board sizes, fixes a caching issue
            board_key = f"sudoku-board-{size}"
            
        return message, color, board_div, board_children, board_style, board_key
    
    """
    checks if number is legal in a sudoku board of size size
    """
    def is_number_valid(self, number: str | None, size: str | None) -> bool:
        return size is not None and number is not None and 0 <= int(number) <= int(size)
    
    """
    called when a sudoku cell is clicked, if the number choice field is legal it writes that number there
    """
    def sudoku_cell_clicked(self, n_clicks, sudoku_cell, cell_style, size, number):
        if not self.is_number_valid(number, size): # invalid number
            return no_update, no_update

        cell_style['color'] = 'black'
        if int(number) == 0:
            sudoku_cell = "" # empty the cell
        else:
            sudoku_cell = str(int(number)) # put the number

        return sudoku_cell, cell_style

    """
    called when the generate random board button is pressed, creates a random board
    with the logic from the Sudoku class, and turns it into html
    """
    def generate_random_sudoku(self, n_clicks, size):
        message = "Board generated successfully!"
        color = {'color': 'black'}
        # creating a sudoku object for random board generation
        sudoku = Sudoku.initializeRandomly(int(size))
        # creating the html board
        board_children = self.create_sudoku_board(int(size), sudoku.board)
        return message, color, board_children
    
    """
    takes a frontend sudoku board as a list of cells and the size of the board,
    and makes a backend board. treats non black cells as empty ones
    """
    def sudoku_frontend_to_backend(self, sudoku_board, size: int) -> list[list[int | None]]:
        board = [[None for _ in range(size)] for _ in range(size)] # empty backend board
        for cell in sudoku_board:
            row: int = int(cell['props']['id']['row'])
            column: int = int(cell['props']['id']['col'])
            text: str = cell['props']['children']
            color: str = cell['props']['style']['color']
            if text != "" and color == 'black': # if filled by the user
                board[row][column] = int(text) - 1 # 1 index to 0 index
        return board
    
    """
    takes the current frontend board as sudoku_board and the backend board as board.
    changes the frontend according to the backend solution. assumes all backend cells
    are non empty. keeps the full frontend cells filled by the user (black), and puts
    the new values in the rest of the cells, all new values are colored blue
    """
    def sudoku_backend_to_frontend(self, sudoku_board, board):
        version = str(uuid4()) # unique id, fixes a memory bug 
        for cell in sudoku_board:
            cell['props']['id']['version'] = version
            row: int = int(cell['props']['id']['row'])
            column: int = int(cell['props']['id']['col'])
            text: str = cell['props']['children']
            color: str = cell['props']['style']['color']
            if text != "" and color == 'black': # if filled by user
                continue
            text = str(board[row][column] + 1) # 0 index to 1 index
            color = 'blue'
            cell['props']['children'] = text
            cell['props']['style']['color'] = color
        return sudoku_board
    