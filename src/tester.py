"""
this file is for internal testing purposes
to use it, run test_solver() with the solver you want to test
it will run through all tests the array testcases
the array testcase_answers should contain true if the testcase is solvable, and false otherwise

"""

from SAT import AbstractSATSolver 
from sudoku import Sudoku
from graph_coloring import GraphColoring
from hamiltonian_cycle import HamiltonianCycle
from SAT_reducible_problem import SATReducibleProblem
import datetime
from time import sleep
from constants import DEFAULT_SOLVER
# dependency: pip install termcolor
from termcolor import colored


"""
Explanation for the testcases:

1. resources extreme 9x9 sudoku
2. resources hard 9x9 sudoku
3. resources expert 9x9 sudoku
4. unsolvable 4x4 sudoku
5. random dense 3-colorable 10-node graph
6. random dense 2-colorable 15-node graph
7. 10-node graph that is not 3-colorable(has a 4-clique)
8. 15-node graph that is not 2-colorable(has a 3-clique)
9. 3-coloring the Grötzsch graph - 11-node graph that is triangle free but not 3-colorable
10. 4-coloring the Grötzsch graph
11. 15-node dense graph with hamcycle
12. hamcycle in a graph that is a cycle of 15
13. hamcycle in a 10-node graph that is two unconnected 5-cliques
"""
testcases = [
    Sudoku(Sudoku.convert_board([
        [3, 0, 0, 0, 4, 9, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 5, 0, 1],
        [7, 5, 2, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 7, 0, 0],
        [5, 0, 0, 3, 9, 6, 0, 0, 0],
        [0, 0, 8, 1, 5, 0, 0, 9, 6],
        [0, 0, 3, 0, 1, 0, 0, 6, 0],
        [0, 0, 4, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 2, 8, 0, 0, 0]
    ])),
    Sudoku(Sudoku.convert_board([
        [1, 0, 0, 0, 3, 4, 0, 0, 8],
        [0, 7, 0, 6, 8, 0, 0, 3, 0],
        [0, 0, 8, 2, 1, 0, 7, 0, 4],
        [0, 5, 4, 0, 9, 0, 6, 8, 0],
        [9, 1, 0, 5, 0, 8, 0, 2, 0],
        [0, 8, 0, 3, 0, 0, 0, 0, 5],
        [3, 0, 5, 9, 0, 6, 8, 7, 1],
        [0, 0, 6, 0, 0, 0, 0, 4, 0],
        [0, 0, 1, 0, 7, 0, 2, 0, 0]
    ])),
    Sudoku(Sudoku.convert_board([
        [1, 5, 0, 0, 8, 2, 0, 0, 0],
        [3, 0, 0, 0, 7, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 7, 5, 3],
        [0, 0, 0, 5, 2, 7, 6, 0, 9],
        [0, 0, 0, 0, 0, 0, 5, 0, 0],
        [0, 4, 0, 0, 6, 3, 8, 0, 7],
        [4, 0, 0, 0, 0, 8, 0, 0, 0],
        [7, 0, 3, 0, 4, 0, 1, 0, 0],
        [0, 0, 8, 6, 0, 0, 3, 0, 0]
    ])),
    Sudoku(Sudoku.convert_board([
        [1, 0, 0, 0],
        [0, 0, 0, 2],
        [0, 0, 0, 0],
        [0, 0, 1, 0]
    ])),
    GraphColoring(10, 
                  [[0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [1, 2], [1, 3], [1, 4], [2, 3], [2, 5], [2, 6], [2, 7], [2, 9], [3, 5], [3, 7], [3, 8], [3, 9], [4, 5], [4, 8], [4, 9], [5, 6], [6, 7], [6, 8], [6, 9]],
                  [None for i in range(10)], 3),
    GraphColoring(15,
                  [[0, 2], [0, 3], [0, 4], [0, 7], [0, 8], [0, 13], [0, 14], [1, 3], [1, 4], [1, 8], [1, 13], [2, 5], [2, 10], [2, 11], [2, 12], [3, 5], [3, 6], [3, 9], [3, 11], [3, 12], [4, 5], [4, 6], [4, 9], [4, 10], [4, 11], [4, 12], [5, 7], [5, 8], [6, 7], [6, 8], [6, 13], [8, 9], [8, 10], [8, 11], [8, 12], [9, 13], [9, 14], [10, 13], [10, 14], [11, 14], [12, 13], [12, 14]],
                  [None for i in range(15)], 2),
    GraphColoring(10,
                  [[0, 1], [0, 3], [0, 5], [0, 7], [0, 8], [0, 9], [1, 3], [1, 5], [1, 7], [1, 8], [1, 9], [2, 3], [2, 5], [2, 6], [2, 7], [2, 9], [3, 4], [3, 8], [4, 5], [4, 6], [4, 7], [4, 9], [5, 6], [5, 8], [6, 7], [6, 8], [6, 9], [7, 9], [8, 9]],
                  [None for i in range(10)], 3),
    GraphColoring(15,[[0, 1], [0, 2], [0, 4], [0, 6], [0, 9], [0, 10], [0, 12], [0, 14], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 12], [1, 13], [1, 14], [2, 5], [2, 8], [2, 9], [2, 10], [2, 11], [2, 13], [3, 5], [3, 7], [3, 8], [3, 10], [3, 11], [3, 13], [4, 5], [4, 7], [4, 8], [4, 9], [4, 11], [4, 13], [5, 6], [5, 9], [5, 10], [5, 12], [5, 14], [6, 7], [6, 9], [6, 10], [6, 13], [7, 9], [7, 10], [7, 12], [7, 14], [8, 9], [8, 10], [8, 12], [8, 14], [9, 11], [9, 14], [10, 11], [10, 12], [10, 14], [11, 12], [12, 13]],
                  [None for i in range(15)], 2),
    GraphColoring(11, [[0,1],[0,2],[1,3],[2,3],[2,5],[1,4],[4,6],[3,6],[5,7],[3,7],[3,9],[6,8],[7,10],[8,9],[9,10],[0,10],[5,8],[10,4],[8,0],[4,5]],
                  [None for i in range(11)], 3),
    GraphColoring(11, [[0,1],[0,2],[1,3],[2,3],[2,5],[1,4],[4,6],[3,6],[5,7],[3,7],[3,9],[6,8],[7,10],[8,9],[9,10],[0,10],[5,8],[10,4],[8,0],[4,5]],
                  [None for i in range(11)], 4),
    HamiltonianCycle(15, [[0, 4], [0, 8], [0, 9], [0, 10], [0, 11], [0, 12], [0, 14], [1, 6], [1, 8], [1, 9], [1, 10], [1, 11], [1, 12], [2, 3], [2, 4], [2, 5], [2, 6], [2, 8], [2, 9], [2, 11], [2, 14], [3, 6], [3, 8], [3, 9], [3, 10], [3, 12], [3, 13], [3, 14], [4, 6], [4, 7], [4, 8], [4, 12], [4, 13], [5, 6], [5, 7], [5, 9], [5, 10], [5, 13], [6, 7], [6, 8], [6, 9], [6, 10], [6, 11], [6, 12], [6, 14], [7, 9], [7, 10], [7, 12], [7, 13], [8, 11], [8, 12], [9, 12], [9, 14], [10, 13], [11, 12], [11, 13], [12, 13]]),
    HamiltonianCycle(15, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14], [14, 0]]),
    HamiltonianCycle(10, [[0, 1], [0, 2], [0, 3], [0, 4], [1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4], [5, 6], [5, 7], [5, 8], [5, 9], [6, 7], [6, 8], [6, 9], [7, 8], [7, 9], [8, 9]])
]

testcase_answers = [
    True,
    True,
    True,
    False,
    True,
    True,
    False,
    False,
    False,
    True,
    True,
    True,
    False
]

# run the problem, and check it against the correct answer
# returns true is success, false if failure
def run_test(problem: SATReducibleProblem, answer: bool) -> bool:
    try:
        sol = problem.solve()
    except Exception:
        return False
    if (sol is None):
        if (answer):
            return False
        else:
            return True
    else:
        if (answer):
            return problem.validate(sol)
        else:
            return False

# prints the deposition regarding the correctness of the satsolver
# verdict is true if the solver was correct, and false otherwise
def print_deposition(verdict: bool) -> None:

    if (verdict):
        s = """I, the undersigned, {{name}}, holder of ID number {{taz}}, after having been warned that I must tell the truth and that I will be subject to the penalties prescribed by law if I do not do so, hereby declare as follows:

1. I make this affidavit of my own free will, with full knowledge of its legal significance.

2. As part of tests, experiments, and actual use that I carried out on software for solving Boolean satisfiability problems (SAT Solver) (hereinafter: “the system”), I examined its mode of operation and its results.

3. In all the tests I performed, the system provided solutions consistent with expectations and with the results known to me, and no failures were found within the aforementioned tests.

4. Notwithstanding the above, the scope of the tests performed is limited, and therefore I cannot rule out the existence of additional cases in which an incorrect result may occur.

5. This affidavit faithfully reflects my personal and professional impression, in accordance with the data available to me at the time of examining the system.

6. This is my name, this is my signature, and the contents of my affidavit are true.

Signature
{{name}}

Date
{{date}}"""    
    else:
        s = """I, the undersigned, {{name}}, holder of ID number {{taz}}, after having been warned that I must tell the truth and that I will be subject to the penalties prescribed by law if I do not do so, hereby declare as follows:

1. I make this affidavit of my own free will, with full knowledge of its legal significance.

2. As part of tests, experiments, and actual use that I carried out on software for solving Boolean satisfiability problems (SAT Solver) (hereinafter: “the system”), I examined its mode of operation and its results.

3. During the tests I performed, cases were found in which the system did not provide solutions consistent with expectations or with the results known to me, and failures in its operation were also identified.

4. In light of these findings, in my assessment the system does not operate properly or reliably in all cases.

5. This affidavit faithfully reflects my personal and professional impression, in accordance with the data available to me at the time of examining the system.

6. This is my name, this is my signature, and the contents of my affidavit are true.

Signature
{{name}}

Date
{{date}}"""
    s = s.replace("{{name}}", "Gabriel Shoef")
    s = s.replace("{{taz}}", "215869819")
    s= s.replace("{{date}}", str(datetime.date.today()))
    print(s)


# run all the testcases
def test_solver(solver: AbstractSATSolver) -> None:
    tests_passed = 0
    for i in range(len(testcases)):
        test = str(i+1)
        if (len(test) == 1):
            test = "0" + test
        print("running test",test,": ",end="")
        testcases[i].setsolver(solver)
        verdict = run_test(testcases[i], testcase_answers[i])
        if (verdict):
            print(colored("ACCEPTED","green"))
            tests_passed += 1
        else:
            print(colored("WRONG ANSWER","red"))
    print("-------------------------------------------------------")
    print("passed",tests_passed,"/",len(testcases),"tests")
    if (tests_passed == len(testcases)):
        print(colored("All tests passed!","green"))
    else:
        print(colored("Some tests failed!","red"))
    print("-------------------------------------------------------")
    print("PRINTING LEGAL NOTICE REGARDING THE VALIDITY OF THIS TESTING PROCEDURE")
    sleep(2)
    print("-------------------------------------------------------")
    print_deposition(tests_passed == len(testcases))
    print("-------------------------------------------------------")

def main():
    test_solver(DEFAULT_SOLVER)
    

if __name__ == "__main__":
    main()