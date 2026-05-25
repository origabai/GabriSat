from graph_coloring import GraphColoring
from sudoku import Sudoku
from hamiltonian_cycle import HamiltonianCycle
from time_tester import test_time
from constants import CPP_BacktrackingSolver_V2, CPP_IDHamcycleSolver, CPP_IDColoringSolver

def benchmark_times():
    print("Starting time benchmark")
    # print(
    #     "Average time to 20-color a 40 vertex graph:",
    #     test_time(GraphColoring.generate(), 225, satsolver=CPP_IDColoringSolver),
    # )
    # print(
    #     "Average time to find a hamiltonian cycle on a 40 vertex graph:",
    #     test_time(HamiltonianCycle.generate(), 200, trials = 10, satsolver=CPP_IDHamcycleSolver),
    # )
    print(
        "Average time to solve a 16x16 sudoku:",
        test_time(Sudoku.generate(), 16, trials=10, satsolver=CPP_BacktrackingSolver_V2),
    )
    
def main():
    benchmark_times()

if __name__ == "__main__":
    main()