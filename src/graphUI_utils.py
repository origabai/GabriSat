from dash import Dash, html, Input, Output, State, dcc
import dash_cytoscape as cyto
import _thread
from random import randint
from graph_coloring import GraphColoring
from hamiltonian_cycle import HamiltonianCycle
from constants import RandomGraphMinSize, RandomGraphMaxSize, ColourSelectorOptions
from graphUI_layout import GraphUILayout
"""
provides utils for graph_visualizer.py
"""
class GraphUtils:
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
    @staticmethod
    def generate_initial_graph_data(nodes, edges, colors = None, special_edges = None):
        #handle zero input
        if colors is None:
            colors = ["grey"] * nodes
        if special_edges is None:
            special_edges = []
        
        initial_data = []
        
        #generates nodes in initial_data
        for node in range(nodes):
            initial_data.append({'data' : {'id': str(node), 'label' : str(node), 'color': colors[node]}})
        
        #adds edges -  special edges are a list of edges to colour green. long if statement for undigraph support
        for edge in edges:
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
        
    
    
    
    def handle_mode_change(self, new_mode, current_elements):
        #changing to hampath - we need to clear all colors of the graph's nodes.
        if new_mode == "HAMPATH":
            if current_elements is not None and current_elements != []:
                new_elements = []
                for element in current_elements:
                    if element['data']['color'] == "ForestGreen":
                        new_elements.append(element)
                    else:
                        new_element = element
                        element['data']['color'] = "grey"
                        new_elements.append(new_element)
            else:
                new_elements = []
            #returns cleared out nodes and hides color parts
            return  {'display': 'none'}, {'display': 'none'}, {'display': 'none', 'width': '300px', 'marginTop': '5px'}, {'display': 'none', 'width': '300px', 'marginTop': '5px'}, new_elements

        elif new_mode == "COLOR":
            #when switching to color we need to clear out all coloured edges
            if current_elements is not None and current_elements != []:
                new_elements = []
                for element in current_elements:
                    if element['data']['color'] == "ForestGreen":
                        new_element = element
                        element['data']['color'] = "grey"
                        new_elements.append(new_element)
                    else:
                        new_elements.append(element)
            else:
                new_elements = []
            #unhides the color stuff from the html page
            return  {'display': 'block'}, {'display': 'block'}, {'display': 'block', 'width': '300px', 'marginTop': '5px'}, {'display': 'block', 'width': '300px', 'marginTop': '5px'}, current_elements

        else:
            #this is the mode for finishing simulation
            return  {'display': 'none'}, {'display': 'none'}, {'display': 'none', 'width': '300px', 'marginTop': '5px'}, {'display': 'none', 'width': '300px', 'marginTop': '5px'}, current_elements
    
    #checks if an element is of a colour alligning with the selected one.
    def check_element_compliance(self, element, color):
        try:
            return self.vis_object.color_to_num(element['data']['color']) < int(color) 
        except:
            return True
        
        
    #handles colour number change
    def handle_color_num_change(self, value, current_elements):
        #when no graph does trivial stuff to avoid iteration error
        if current_elements is None or current_elements == []:
            return ColourSelectorOptions[:int(value)+2], []
        
        #changes up the values of all nodes
        new_elements = []
        for element in current_elements:
            if self.check_element_compliance(element, value):
                new_elements.append(element)
            else:
                new_element = element
                element['data']['color'] = "grey"
                new_elements.append(new_element)
                
        #also changes the settings of the options
        return ColourSelectorOptions[:int(value)+2], new_elements
        
    def process_node_click(self, tapped_node, current_elements, selected_colour ,erase_mode, max_num, current_mode):
        # Base case: The app just loaded, and no node has been clicked yet.
        if tapped_node is None:
            return current_elements
        if erase_mode['toggled']:
            
            # Extract the mathematical or topological data from the dictionary
            node_id = tapped_node.get('id', 'Unknown')
            #node_label = tapped_node.get('label', 'No Label')
            # Return formatted HTML to update the DOM
            return [element for element in current_elements if not(
                    element['data']['id'] == node_id or
                    ('source' in element['data'] and element['data']['source'] == node_id) or
                    ('target' in element['data'] and element['data']['target'] == node_id))
                    ]   
        else:
            trivial_conditions = current_mode != "COLOR" or selected_colour[0] is None 
            if trivial_conditions or (selected_colour != "grey" and self.vis_object.color_to_num(selected_colour) > int(max_num) - 1):
                return current_elements
            
            # Extract the mathematical or topological data from the dictionary
            node_id = str(tapped_node.get('id', 'Unknown'))
            
            elements = [element for element in current_elements if element['data']['id'] != node_id]
            elements.append({'data' : {'id' : node_id, 'label' : node_id, 'color' : selected_colour}})
            #node_label = tapped_node.get('label', 'No Label')
            # Return formatted HTML to update the DOM
            return elements 
    
    '''
    generates random graph
    '''
    def generate_random_graph(self, n_clicks, current_elements):
        #handles automatic activation at creation
        if n_clicks == 0:
            return current_elements
        #generates and updates new graph
        new_graph = GraphColoring.generate(size = randint(RandomGraphMinSize, RandomGraphMaxSize))
        return GraphUtils.generate_initial_graph_data(new_graph.num_nodes, new_graph.edges, new_graph.num_nodes*["grey"])
    
    
    def erase_clicked_edge(self, tapped_edge, current_elements, erase_mode):
        # Base case: The app just loaded, and no node has been clicked yet.
        if tapped_edge is None or not erase_mode['toggled']:
            return current_elements
        # Extract the mathematical or topological data from the dictionary
        edge_src = tapped_edge.get('source', 'Unknown')
        edge_target = tapped_edge.get('target', 'Unknown')
        #node_label = tapped_node.get('label', 'No Label')
        # Return formatted HTML to update the DOM
        return [element for element in current_elements if not(
            (('source' in element['data'] and element['data']['source'] == edge_src) and
            ('target' in element['data'] and element['data']['target'] == edge_target)) or
            ('source' in element['data'] and element['data']['source'] == edge_target) and
            ('target' in element['data'] and element['data']['target'] == edge_src))    
            ] 
    
    
    def end_visualization(self, n_clicks, elements, max_colors, problem):
        if n_clicks == 0:
            return 0
        
        #counts the edges and vertices of the graph
        nodes = set([])
        self.vis_object.edges = []
        for element in elements:
            if 'source' not in element['data']:
                nodes.add(int(element['data']['id']))
                self.vis_object.color_storage_for_termination.append([int(element['data']['id']), self.vis_object.color_to_num(element['data']['color'])])
            else:
                self.vis_object.edges.append([int(element['data']['source']), int(element['data']['target'])])
        if nodes == set([]):
            missing_nodes = set([])
        else:
            missing_nodes = set(range(max(nodes))) - nodes
        missing_list = sorted(list(missing_nodes), reverse=True)
            
            
        self.vis_object.max_colors = int(max_colors[0])
        self.vis_object.num_nodes = len(nodes)
        #then, removes non existant vertices to comply with graph_coloring problem
        for node in missing_list:
            for edge in self.vis_object.edges:
                for index in [0,1]:
                    if int(edge[index]) > node:
                        edge[index] -= 1
            for color_node in self.vis_object.color_storage_for_termination:
                if color_node[0] > node:
                    color_node[0] -= 1
            
        self.vis_object.color_storage_for_termination.sort(key = lambda tup : tup[0])
        color_array = [element[1] for element in self.vis_object.color_storage_for_termination]
        self.vis_object.graph = GraphColoring(self.vis_object.num_nodes, self.vis_object.edges, color_array, self.vis_object.max_colors)
        self.vis_object.color_storage_for_termination = []
        found_solution = True
        end_flag = False
        solution = [None] * self.vis_object.num_nodes
        Ham_solution = None
        match problem:
            case "COLOR":
                # solve coloring problem
                print(self.vis_object.graph.colors)
                solution = self.vis_object.graph.solve()
                print(solution)
                print(self.vis_object.graph.colors)
                if solution is None:
                    solution = [None] * self.vis_object.num_nodes
                    found_solution = False
                
            case "HAMPATH":
                # solve hampath problem
                ham_graph = HamiltonianCycle(self.vis_object.graph.num_nodes, self.vis_object.graph.edges)
                Ham_solution = ham_graph.solve()
                if Ham_solution is None:
                    found_solution = False
                #continue
            case "END":
                # end simulation
                end_flag = True   
        
        #and now - terminate the process!
        if end_flag:
            self.vis_object.correct_end = True
            _thread.interrupt_main()
            return "The program finished running. ", {'color' : 'blue'}, GraphUtils.generate_initial_graph_data(0, [], [], [])
        else:
            #print(solution)
            next_colors = [self.vis_object.color_gen(color) for color in solution]
            special_edges = self.vis_object.generate_edges(Ham_solution)
            if found_solution:
                return "Everything good, proceed!", {'color' : 'green'}, GraphUtils.generate_initial_graph_data(self.vis_object.graph.num_nodes, self.vis_object.graph.edges, next_colors, special_edges)
            else:
                return "No solution found!", {'color' : 'red'}, GraphUtils.generate_initial_graph_data(self.vis_object.graph.num_nodes, self.vis_object.graph.edges, next_colors, special_edges)
        #os.kill(os.getpid(), signal.SIGINT)
        return "...this is an error..."