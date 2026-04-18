from math import sqrt, isqrt
from graph_coloring import GraphColoring
from random import randint, shuffle
from SAT_reducible_problem import SATReducibleProblem
from constants import DEFAULT_SOLVER
from SAT import AbstractSATSolver
#from sudoku_generate import generate_sudoku_seed

"""
Sudoku class
the board is an N x N list of ints, representing the colors(0-indexed)
or None if no scolor is set. N must be a square number
"""


class Sudoku(SATReducibleProblem):
    def __init__(self, board: list[list[int | None]], solver = DEFAULT_SOLVER) -> None:
        super().__init__(solver)
        self.board = board
        self.board_size: int = len(board)
        self.square_size: int = int(
            sqrt(self.board_size)
        )  # size of the squares of the sudoku

    # converts board from display format (1 indexed, and 0 meaning blanks)
    # to the format used by the constructor(0 indexed, and None meaning blanks)
    @classmethod
    def convert_board(self, board: list[list[int]]) -> list[list[int | None]]:
        b = board.copy()
        for i in range(len(b)):
            for j in range(len(b[i])):
                if (b[i][j] == 0):
                    b[i][j] = None
                else:
                    b[i][j] -= 1
        return b

    def validate(self, board: list[list[int]]):
        sq = isqrt(len(board))
        if (sq * sq != len(board)):
            return False        
        # check rows and collumns
        for i in range(len(board)):
            row = []
            col = []
            for j in range(len(board)):
                row.append(board[i][j])
                col.append(board[i][j])
            row.sort()
            col.sort()
            if (row != [i for i in range(len(board))]):
                return False
            if (col != [i for i in range(len(board))]):
                return False
        # check squares
        for i in range(len(board) // sq):
            for j in range(len(board) // sq):
                square = []
                for x in range(sq):
                    for y in range(sq):
                        square.append(board[sq*i + x][sq*j + y])
                square.sort()
                if (square != [i for i in range(len(board))]):
                    return False

        return True

    # returns a board with numbers representing a valid solution, or None if none exist
    def solve(self) -> list[list[int]] | None:
        graph_reduction: GraphColoring = self.reduceToGraphColoring()
        sat_reduction: AbstractSATSolver = graph_reduction.reduce_to_SAT()
        sq = isqrt(self.board_size)
        for color in range(self.board_size):
            for i in range(self.board_size):
                    # collumns
                    sat_reduction.addClause([(i*self.board_size + j)*self.board_size + color for j in range(self.board_size)],[])
                    # rows
                    sat_reduction.addClause([(j*self.board_size + i)*self.board_size + color for j in range(self.board_size)],[])
            # squares
            for i in range(sq):
                for j in range(sq):
                    square = []
                    for x in range(sq):
                        for y in range(sq):
                            square.append(((sq*i+x)*self.board_size + (sq*j+y))*self.board_size + color)
                    sat_reduction.addClause(square, [])


        solution: list[int] | None = graph_reduction.reconstruct_solution_from_reduction(sat_reduction.solve())
        if solution is None:
            return None
        return self.reconstructSolutionFromReduction(solution)

    @classmethod
    # creates a new Sudoku object from input
    def initializeFromInput(self):
        board_size = int(
            input("Please input the size of the board (must be a square number): ")
        )
        if (isqrt(board_size)**2 != board_size):
            print("I SAID MUST BE A SQUARE NUMBER")
            return None
        board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        print(
            f"Please now input the board in {board_size} separate lines, each containing {board_size} numbers\n\
the numbers should be from 1 to {board_size}, or 0 if the cell is empty"
        )
        for i in range(board_size):
            input_string: str = input()
            input_list: list[str] = input_string.split(" ")
            for j in range(board_size):
                board[i][j] = int(input_list[j])
                if board[i][j] == 0:
                    board[i][j] = None
                else:
                    board[i][j] -= 1
        return Sudoku(board)

    @classmethod
    # creates a new random Sudoku object of size board_size
    def initializeRandomly(self, board_size: int, satsolver = DEFAULT_SOLVER):
        
        #board = self.generateTrivialBoard(board_size)
        #this is a shinier version!
        board = self.generateInterestingSolvedBoard(board_size)
        coords_to_keep: set[tuple[int, int]] = set()
        while len(coords_to_keep) < board_size ** 1.5:  # board_size ** 1.5 is magic number i think looks good
            i: int = randint(0, board_size)
            j: int = randint(0, board_size)
            coords_to_keep.add((i, j))
        for i in range(board_size):
            for j in range(board_size):
                if (i, j) not in coords_to_keep:
                    board[i][j] = None  # deleting unwanted cells
        
        #return Sudoku(self.generateInterestingSolvedBoard(board_size), solver=satsolver)
        return Sudoku(board, solver=satsolver)

    
    
    @classmethod
    def generate(self, size = 2, solver = DEFAULT_SOLVER):
        return self.initializeRandomly(size, satsolver=solver)

    # returns a new GraphColoring object with a reduction from the sudoku board
    def reduceToGraphColoring(self) -> GraphColoring:
        edges: list[list[int]] = []
        colors: list[int] = []

        for id in range(self.board_size**2):
            i, j = self.idToCoordinate(id)
            colors.append(self.board[i][j])  # initializing colors

        for row in range(self.board_size):
            for i in range(self.board_size):
                for j in range(i + 1, self.board_size):
                    id1: int = self.coordinateToId(row, i)
                    id2: int = self.coordinateToId(row, j)
                    edges.append([id1, id2])
                    # elements in the same row must be unique

        for column in range(self.board_size):
            for i in range(self.board_size):
                for j in range(i + 1, self.board_size):
                    id1: int = self.coordinateToId(i, column)
                    id2: int = self.coordinateToId(j, column)
                    edges.append([id1, id2])
                    # elements in the same column must be unique

        for square_row in range(
            0, self.board_size, self.square_size
        ):  # iterating over squares
            for square_column in range(0, self.board_size, self.square_size):
                for row1 in range(
                    square_row, square_row + self.square_size
                ):  # iterating over first element in the square
                    for column1 in range(
                        square_column, square_column + self.square_size
                    ):
                        for row2 in range(
                            square_row, square_row + self.square_size
                        ):  # iterating over second element in the square
                            for column2 in range(
                                square_column, square_column + self.square_size
                            ):
                                id1: int = self.coordinateToId(row1, column1)
                                id2: int = self.coordinateToId(row2, column2)
                                if id1 == id2:  # doesn't matter
                                    continue
                                edges.append([id1, id2])
                                # elements in the same square nums be unique

        for edge in edges:
            edge.sort()  # making sure edges are sorted for uniqueness
        edges = [
            list(x) for x in dict.fromkeys(tuple(x) for x in edges)
        ]  # getting rid of duplicate edges

        return GraphColoring(
            num_nodes=self.board_size**2,
            edges=edges,
            colors=colors,
            max_colors=self.board_size,
            satsolver=self.solver
        )

    # takes a valid solution of the reduction graph as a list of ints representing colors,
    # and returns a solution for the sudoku as an N x N list of ints
    def reconstructSolutionFromReduction(self, solution: list[int]) -> list[list[int]]:
        solved_board: list[list[int]] = [
            [0 for _ in range(self.board_size)] for _ in range(self.board_size)
        ]
        for id, color in enumerate(solution):
            i, j = self.idToCoordinate(id)
            solved_board[i][j] = color
        return solved_board

    # takes a coordinate in the sudoku board and returns the id of the node in the reduction graph
    def coordinateToId(self, i: int, j: int) -> int:
        return i * self.board_size + j

    # takes an id of a node in the reduction graph and returns the coordinates in the sudoku board
    def idToCoordinate(self, id: int) -> tuple[int, int]:
        return id // self.board_size, id % self.board_size

    @staticmethod
    # returns a two dimensional list of ints with the trivial solution of a sudoku
    def generateTrivialBoard(board_size: int) -> list[list[int]]:
        board: list[list[int]] = [
            [i for i in range(board_size)] for _ in range(board_size)
        ]
        square_size: int = int(sqrt(board_size))
        for square_row in range(0, board_size, square_size):
            # magically make the trivial solution, trust me bro
            board[square_row] = [
                (x + (square_row // square_size)) % board_size
                for x in board[square_row]
            ]
            for row in range(square_row + 1, square_row + square_size):
                board[row] = [
                    (x + square_size * (row - square_row)) % board_size
                    for x in board[square_row]
                ]
        return board
    
    @classmethod
    def generateInterestingSolvedBoard(self, board_size: int, satsolver = DEFAULT_SOLVER) -> list[list[int]]:
        solution = None
        while solution is None:
            board_seed = self.sudokuSeedGen(board_size)
            sudoku_gen = Sudoku(board_seed, solver=satsolver)
            solution = sudoku_gen.solve()
        return solution #for now return only working boards
    
    @classmethod
    def sudokuSeedGen(self, size : int) -> list[list[int | None]]:
        #seeding row
        board = [[None] * size for _ in range(size)]
        values = [i for i in range(size)]
        shuffle(values)
        board[0] = values[:]
        
        #editing other rows for non-triviality
        shuffled_vals = self.randomDerangement(values)
        for i in range(int(sqrt(size))):
            j = randint(int(sqrt(size)), size - 1)
            board[j][i] = shuffled_vals[i]
        
        return board
    
    @staticmethod
    #generates random arrangement of an array without fixed points.
    #used for unique seeding.
    def randomDerangement(arr):
        n = len(arr)
        res = list(arr)
        while True:
            shuffle(res)
            if all(res[i] != arr[i] for i in range(n)):
                return res