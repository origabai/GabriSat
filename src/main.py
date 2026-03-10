from graph_coloring import GraphColoring
from sudoku import Sudoku
from visualizer import Visualizer

def main():
    graph = GraphColoring(6, [[0,1],[0,2],[1,2],[2,3],[2,5],[5,4],[3,4]], [1,2,6,7,None,None], 3)
    # print(g.solve())
    vis = Visualizer(graph)
    graph = vis.show()
    
    solution = graph.solve()
    
    vis = Visualizer(graph, solution)
    vis.show()
    #s = Sudoku.initializeRandomly(9)
    #print(s.reduceToGraphColoring().edges)

if __name__ == "__main__":
    main()