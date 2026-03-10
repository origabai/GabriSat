from graph_coloring import GraphColoring
from sudoku import Sudoku
from visualizer import Visualizer
from hamiltonian_cycle import HamiltonianCycle
from time_tester import test_time
def main():
    # g = GraphColoring(6, [[0,1],[0,2],[1,2],[2,3],[2,5],[5,4],[3,4]], [None,None,None,None,None,None], 3)
    # print(g.solve())
    print(test_time(GraphColoring.generate(), 6))
    print(test_time(HamiltonianCycle.generate(), 4))
    print(test_time(Sudoku.generate(), 1))
    
    print("STARTING VISUAL EPICNESS")
    
    graph = GraphColoring(6, [[0,1],[0,2],[1,2],[2,3],[2,5],[5,4],[3,4]], [1,2,6,7,None,None], 3)
    # print(g.solve())
    vis = Visualizer(graph)
    graph = vis.show()
    
    solution = graph.solve()
    
    vis = Visualizer(graph, solution)
    vis.show()

if __name__ == "__main__":
    main()