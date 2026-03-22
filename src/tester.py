"""
this file is for internal testing purposes
to use it, run test_solver() with the solver you want to test
it will run through all tests in testing/testcases
each test is a txt file of the following format:

num_variables num_clauses
num_pos_variables_1
pos_variables_1
num_neg_variables_1
neg_variables_1
...
num_pos_variables_m
pos_variables_m
num_neg_variables_m
neg_variables_m

SAT/UNSAT if the problem is satisfiable or not

"""

from SAT import AbstractSATSolver, SATClause
import os
import datetime
# dependency: pip install python-bidi
from bidi.algorithm import get_display
from time import sleep
from constants import DEFAULT_SOLVER
from hamiltonian_cycle import HamiltonianCycle
# dependency: pip install termcolor
from termcolor import colored

# loads a sat problem from a file according to the above format
# returns a the number of variabls, a list of the clauses and the correct answer
def load_sat_from_file(test_file: str) -> tuple[int,list[SATClause],str]:
    with open(test_file) as f:
        # get first parameters
        contents = f.read().split("\n")
        num_variables, num_clauses = [int(x) for x in contents[0].split(" ")]
        clauses: list[SATClause] = []
        idx = 0
        # load all clauses
        for i in range(num_clauses):
            pos = []
            neg = []

            # load pos
            idx += 1
            num_pos_variables = int(contents[idx])
            for j in range(num_pos_variables):
                idx += 1
                pos.append(int(contents[idx]))
            
            # load neg
            idx += 1
            num_neg_variables = int(contents[idx])
            for j in range(num_neg_variables):
                idx += 1
                neg.append(int(contents[idx]))
            clauses.append(SATClause(pos, neg))
        return num_variables, clauses, contents[-1]

# checks whether a solution satisfies the satproblem given by clauses
# returns true if correct, false otherwise
def check_sat_solution(clauses: list[SATClause], sol: list[bool | None]) -> bool:
    for c in clauses:
        val = False
        for x in c.pos_variables:
            if (sol[x]):
                val = True
                break
        for x in c.neg_variables:
            if (not sol[x]):
                val = True
                break
        if (not val):
            return False
    return True
    

# run the test from test_file
# returns true is success, false if failure
def run_test(test_file: str, solver: AbstractSATSolver) -> bool:
    num_variables, clauses, answer = load_sat_from_file(test_file)
    sat : AbstractSATSolver = solver(num_variables)
    for c in clauses:
        sat.addClause(c.pos_variables, c.neg_variables)
    try:
        sol = sat.solve()
    except Exception:
        return False
    if (sol is None):
        if (answer == "UNSAT"):
            return True
        else:
            return False
    else:
        if (answer == "UNSAT"):
            return False
        else:
            return check_sat_solution(clauses, sol)

# prints the deposition regarding the correctness of the satsolver
# verdict is true if the solver was correct, and false otherwise
def print_deposition(verdict: bool) -> None:
    file = os.path.dirname(os.path.abspath(__file__)) + os.sep + "testing" + os.sep
    if (verdict):
        file += "deposition_AC.txt"
    else:
        file += "deposition_WA.txt"
    with open(os.path.abspath(file), encoding="utf-8") as f:
        s = f.read()
        s = s.replace("{{name}}", "גבריאל שואף")
        s = s.replace("{{taz}}", "215869819")
        s= s.replace("{{date}}", str(datetime.date.today()))
        print(get_display(s))


# run all the tests in testing/testcases
def test_solver(solver: AbstractSATSolver) -> None:
    i = 0
    tests_passed = 0
    TESTS_PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep + "testing" + os.sep + "testcases"
    for test_file in os.listdir(TESTS_PATH):
        i+=1
        test = str(i)
        if (len(test)==1):
            test = "0" + test
        print("running test",test,": ",end="")
        verdict = run_test(TESTS_PATH + os.sep + test_file, solver)
        if (verdict):
            print(colored("ACCEPTED","green"))
            tests_passed += 1
        else:
            print(colored("WRONG ANSWER","red"))
    print("-------------------------------------------------------")
    print("passed",tests_passed,"/",i,"tests")
    if (tests_passed == i):
        print(colored("All tests passed!","green"))
    else:
        print(colored("Some tests failed!","red"))
    print("-------------------------------------------------------")
    print("PRINTING LEGAL NOTICE REGARDING THE VALIDITY OF THIS TESTING PROCEDURE")
    sleep(2)
    print("-------------------------------------------------------")
    print_deposition(tests_passed == i)
    print("-------------------------------------------------------")

def main():
    test_solver(DEFAULT_SOLVER)
    

if __name__ == "__main__":
    main()