import matplotlib.pyplot as plt

class SudokuVisualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

    """
    visualizes a sudoku board. empty squares are noted by None
    """
    def visualize_sudoku(self, board):
        if board is None:
            print("no solution")
            return
        plt.cla()
        # make axes the same scale ane make them disappear
        self.ax.set_box_aspect(1)
        self.ax.axis('off')
        # replace None's with empty strings
        for i in range(len(board)):
            for j in range(len(board[i])):
                if (board[i][j] is None):
                    board[i][j] = ""
        # plot the board
        self.ax.table(cellText=board,cellLoc='center', bbox=[0.25, 0.25, 0.5, 0.5])
        plt.show(block=False)

