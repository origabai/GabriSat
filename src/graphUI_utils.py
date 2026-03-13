from dash import Dash, html, Input, Output, State, dcc
import dash_cytoscape as cyto
import _thread
from random import randint
from graph_coloring import GraphColoring
from hamiltonian_cycle import HamiltonianCycle
from constants import RandomGraphMinSize, RandomGraphMaxSize, ColourSelectorOptions
from graphUI_layout import GraphUILayout
from constants import CLEAR_LABEL, LABEL, CLEAR_SELECTOR, SELECTOR


"""
provides utils for graph_visualizer.py
"""
class GraphUtils():
    '''
    here are all of the functions that the graphUI uses.
    '''
    
    
    def __init__(self, app : Dash, vis_object):
        '''
        generates layout and initialized function input
        '''
        self.vis_object = vis_object
        self.app = app
        self.layout = GraphUILayout(self).default_layout
    
    '''
    generates initial graph element data. takes in solutions and nodes/edges.
    '''
    
    def generate_initial_graph_data(self, special_edges = []):
        #handle zero input
        graph = self.vis_object.graph
        
        initial_data = []
        #generates nodes in initial_data
        for node in range(graph.num_nodes):
            initial_data.append({'data' : {'id': str(node), 'label' : str(node), 'color': self.vis_object.get_color_at_node(node)}})
        
        #adds edges -  special edges are a list of edges to colour green. long if statement for undigraph support
        for edge in graph.edges:
            initial_data.append({'data' : {'source': str(edge[0]), 'target': str(edge[1]), 'color' : 'grey'}})
            if edge in special_edges or [edge[1], edge[0]] in special_edges:
                initial_data[-1]['data']['color'] = 'ForestGreen'
        
        #exits
        return initial_data
        
    
    def add_node(self, n_clicks, current_elements):
        #finds existing nodes
        current_nodes = [int(element['data']['id']) for element in current_elements if 'target' not in element['data']]
        #finds next node to add
        next_id = min(set(range(0,len(current_nodes)+2))-set(current_nodes))
        # Construct the new node dictionary and append it to the state
        new_node = {'data': {'id': str(next_id), 'label': str(next_id), 'color' : "grey"}}
        current_elements.append(new_node)
        
        return current_elements
        
    #TODO: replace with better add edge capabilities.
    def add_edge(self, n_clicks, source_id, target_id, current_elements):
        if not source_id or not target_id:
            return current_elements # Do nothing if source/target are empty
        
        # Construct the new edge dictionary and append it to the state
        new_edge = {'data': {'source': source_id, 'target': target_id, 'color' : 'grey'}}
        if {'data': {'source': target_id, 'target': source_id, 'color' : 'grey'}} and {'data': {'source': target_id, 'target': source_id, 'color' : 'ForestGreen'}} not in current_elements and new_edge not in current_elements:
            current_elements.append(new_edge)
        
        return current_elements
        
        
    def switch_erasing_mode(self, n_clicks):
        if n_clicks%2 == 0:
            return {'toggled' : False}, {'backgroundColor': 'lightgray', 'color': 'black', 'padding': '10px'}
        else:
            return {'toggled' : True}, {'backgroundColor': 'red', 'color': 'black', 'padding': '10px'}
        
    
    #returns true if an element is an edge
    def is_edge(self, element):
        return 'target' in element['data']
    
    #checks if an element is adjacent to a node
    def is_adjacent_to(self, edge, node_id):
        if edge['data']['id'] == node_id:
            return True
        if not self.is_edge(edge):
            return False
        return node_id in [edge['data']['target'], edge['data']['source']]
    
    #returns true if an element is a node
    def is_node(self, element):
        return not self.is_edge(element)
    
    #util function - colors all elements to grey, depending on the criterion given passed as argument.
    def color_to_grey(self, elements, criterion):
        new_elements = []
        for element in elements:
            new_elements.append(element)
            if criterion(element):
                new_elements[-1]['data']['color'] = "grey"
        return new_elements
    
    
    def handle_mode_change(self, new_mode, current_elements):
        #changing to hampath - we need to clear all colors of the graph's nodes.
        if new_mode == "HAMPATH":
            new_elements = self.color_to_grey(current_elements, self.is_node)
            #returns cleared out nodes and hides color parts
            return  CLEAR_LABEL, CLEAR_LABEL, CLEAR_SELECTOR, CLEAR_SELECTOR, new_elements
        elif new_mode == "COLOR":
            #when switching to color we need to clear out all coloured edges
            new_elements =self.color_to_grey(current_elements, self.is_edge) 
            #unhides the color stuff from the html page
            return  LABEL, LABEL, SELECTOR, SELECTOR, new_elements
        else:
            #this is the mode for finishing simulation
            return  CLEAR_LABEL, CLEAR_LABEL, CLEAR_SELECTOR, CLEAR_SELECTOR, current_elements
    
    
    #checks if an element is of a colour alligning with the selected one - if larger, returns false.
    def check_element_color_compliance(self, element, color):
        if element['data']['color'] == "grey" or element['data']['color'] == "ForestGreen":
            return False
        
        return 1 + self.vis_object.color_to_num(element['data']['color']) > int(color)
    
    
    #handles colour number change
    def handle_color_num_change(self, value, current_elements):
        #options for colour selector - depending on colour.
        next_options = ColourSelectorOptions[:int(value)+2]
        #changes up the values of all nodes
        def compare_color(element):
            return self.check_element_color_compliance(element, value)
        new_elements = self.color_to_grey(current_elements, compare_color)
        #also changes the settings of the options
        return next_options, new_elements
        
        
    def remove_adjacent_edges(self, tapped_node_id, elements):
        return [element for element in elements if not self.is_adjacent_to(element, tapped_node_id)]

    #recolors a node from elements
    def recolor_node(self, elements, color, node_id):
        elements = [element for element in elements if element['data']['id'] != node_id]
        elements.append({'data' : {'id' : node_id, 'label' : node_id, 'color' : color}})
        return elements
        
    
    def process_node_click(self, tapped_node, current_elements, selected_colour ,erase_mode, max_num, current_mode):
        # Base case: The app just loaded, and no node has been clicked yet.
        if tapped_node is None:
            return current_elements
        
        #if erasing:
        if erase_mode['toggled']:
            return self.remove_adjacent_edges(tapped_node['id'], current_elements) 
        else:
            #check need to color depending on selected color
            trivial_conditions = current_mode != "COLOR" or selected_colour is None
            if trivial_conditions or self.vis_object.color_to_num(selected_colour) > int(max_num) - 1:
                return current_elements
            #now, recolor when needed:
            return self.recolor_node(current_elements, selected_colour, tapped_node['id'])
    
    '''
    generates random graph
    '''
    def generate_random_graph(self, n_clicks, current_elements):
        #handles automatic activation at creation
        if n_clicks == 0:
            return current_elements
        #generates and updates new graph
        self.vis_object.graph = GraphColoring.generate(size = randint(RandomGraphMinSize, RandomGraphMaxSize))
        return self.generate_initial_graph_data()
    
    def is_edge_connecting(self, edge, id1, id2):
        if not self.is_edge(edge):
            return False
        else:
            edge_bounds = set([edge['data']['source'], edge['data']['target']])
            return edge_bounds == set([id1, id2])
    
    def erase_edge(self, elements, id1, id2):
        return [element for element in elements if not self.is_edge_connecting(element, id1, id2)]
    
    def process_edge_click(self, tapped_edge, current_elements, erase_mode):
        # remove edge if necessary
        if tapped_edge is not None and erase_mode['toggled']:
            return self.erase_edge(current_elements, tapped_edge['source'], tapped_edge['target'])
        #base case - dont respond if un-needed
        return current_elements
    
    
    def parse_color_for_graph(self, element):
        value = self.vis_object.color_to_num(element['data']['color'])
        
        if value == -1:
            return None
        return value
    
    def parse_current_graph_data(self, elements):
        nodes = []
        node_color_array = []
        edges = []
        
        for element in elements:
            if self.is_node(element):
                new_id = int(element['data']['id'])
                nodes.append(new_id)
                new_color = self.parse_color_for_graph(element)
                node_color_array.append([new_id, new_color])
                
            elif self.is_edge(element):
                edges.append([int(element['data']['source']), int(element['data']['target'])])
        
        return nodes, edges, node_color_array
    
    def smart_index(self, array, index):
        try:
            return array.index(index)
        except ValueError:
            return -1
    
    def reduce_excess_nodes(self, nodes, edges, color_tuples):
        #check for empty case
        if nodes == []:
            return [], [], []
        
        nodes.sort()
        new_value = [self.smart_index(nodes, num) for num in range(max(nodes) + 1)]
        
        #reduce nodes
        nodes = [new_value[node] for node in nodes]
        
        #reduce edges
        edges = [[new_value[edge[0]], new_value[edge[1]]] for edge in edges]
        
        #reduce color tuples:
        color_tuples = [[new_value[tup[0]], tup[1]] for tup in color_tuples]
        
        #return reduced
        return nodes, edges, color_tuples
    
    def construct_new_graph(self, nodes, edges, color_tuples, max_colors):
        color_tuples.sort(key = lambda tup : tup[0])
        color_array = [element[1] for element in color_tuples]
        return GraphColoring(len(nodes), edges, color_array, max_colors)
    
    def construct_graph_from_elements(self, elements, max_colors):
        new_nodes, new_edges, new_color_tuples = self.parse_current_graph_data(elements)
        new_nodes, new_edges, new_color_tuples = self.reduce_excess_nodes(new_nodes, new_edges, new_color_tuples)
        return self.construct_new_graph(new_nodes, new_edges, new_color_tuples, max_colors)
    
    def generate_solved_colors(self):
        solution = self.vis_object.graph.solve()
        if solution is None:
            solution = [None] * self.vis_object.graph.num_nodes
        
        return solution != [None] * self.vis_object.graph.num_nodes, solution
    
    def generate_solved_hampath(self):
        ham_graph = HamiltonianCycle(self.vis_object.graph.num_nodes, self.vis_object.graph.edges)
        ham_solution = ham_graph.solve()
        
        return ham_solution is not None, self.vis_object.generate_edges(ham_solution)
        
    def solve_problems(self, problem):
        new_colors = [None] * self.vis_object.graph.num_nodes
        hampath_edges = []
        
        if problem == "COLOR":
            found_solution, new_colors = self.generate_solved_colors()
        elif problem == "HAMPATH":
            found_solution, hampath_edges = self.generate_solved_hampath()
        else:
            found_solution = False
            
        self.vis_object.graph.colors = new_colors
        new_graph_data = self.generate_initial_graph_data(hampath_edges)
        
        return found_solution, new_graph_data
    
    def end_visualization(self, n_clicks, elements, max_colors, problem):
        #prevent accidental press.
        if n_clicks == 0:
            print("i have no clue how to fix this, thats a bug.")
            return "welcome to the editor!", {'color' : 'black'}, elements
        
        #handle end program:
        if problem == "END":
            self.vis_object.correct_end = True
            _thread.interrupt_main()
            return "The program finished running. ", {'color' : 'blue'}, []
            
        #now, for the interesting case:
        self.vis_object.graph = self.construct_graph_from_elements(elements, int(max_colors))
        print(self.vis_object.graph.colors)
        found_solution, new_graph_data = self.solve_problems(problem)
        
        if found_solution:
            return "Everything good, proceed!", {'color' : 'green'}, new_graph_data
        else:
            return "No solution found!", {'color' : 'red'}, new_graph_data