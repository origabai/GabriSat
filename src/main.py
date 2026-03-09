from graph_coloring import GraphColoring
def main():
    g = GraphColoring(6, [[0,1],[0,2],[1,2],[2,3],[2,5],[5,4],[3,4]], [None,None,None,None,None,None], 3)
    print(g.solve())

if __name__ == "__main__":
    main()