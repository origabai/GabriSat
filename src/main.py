from graph_coloring import GraphColoring
from sudoku import Sudoku
from SAT import SAT
import sys

def main():

    # 1. Check the current recursion limit (usually defaults to 1000)
    current_limit = sys.getrecursionlimit()
    print(f"Current limit: {current_limit}")

    # 2. Set a new recursion limit
    new_limit = 2000
    sys.setrecursionlimit(new_limit)

    print(f"New limit: {sys.getrecursionlimit()}")
    # g = GraphColoring(6, [[0,1],[0,2],[1,2],[2,3],[2,5],[5,4],[3,4]], [None,None,None,None,None,None], 3)
    # g = GraphColoring(4, [[0,1],[0,2],[1,2],[2,3]], [None,None,None,None], 3)
    # g = GraphColoring(3, [[0,1],[0,2],[1,2]], [None,None,None,None], 3)
    # print(g.solve())
    s = Sudoku.initializeRandomly(9)
    print(s.board)
    print(s.solve())
    # s = SAT(3)
    # s.addClause([0, 1, 2], [])
    # s.addClause([], [0, 1])
    # s.addClause([], [1, 2])
    # s.addClause([], [0, 2])
    # print(s.solve())

if __name__ == "__main__":
    main()