"""
this is the python-side endpoint of the cpp-python communication
in order for this to work, add a class inheriting from CPP_SATSolver
to the file cpp_solvers.py
that class's __init__ should set solver_name to be the name
of the cpp solver you want to use
see communication.cpp for the list of names/solvers
"""
from SAT import AbstractSATSolver
from random import choice
import os
"""
A class for communicating with a satsolver written in c++
"""
class CPP_SATSolver(AbstractSATSolver):
    
    """
    creates the class.
    receives as parameters the number of variables,
    as well as a the name of the cpp solver which will be used
    as defined in communication.cpp
    """
    def __init__(self, num_variables, solver_name):
        super().__init__(num_variables)
        self.object_path = os.path.dirname(os.path.abspath(__file__)) + os.sep + "cpp" + os.sep + "communication"
        self.solver_name = solver_name
        
    def solve(self):
        letters = "abcdefghijklmnopqrstuvwxyz"
        # create input file with the correct format
        fname = os.path.dirname(os.path.abspath(__file__)) + os.sep + "".join([choice(letters) for i in range(10)])
        with open(fname + ".in", "w") as f:
            print(self.num_variables, len(self.clauses), file = f)
            for i in range(len(self.clauses)):
                print(len(self.clauses[i].pos_variables),file = f)
                for x in self.clauses[i].pos_variables:
                    print(x, file = f)
                print(len(self.clauses[i].neg_variables),file = f)
                for x in self.clauses[i].neg_variables:
                    print(x, file = f)
        # run the solver
        os.system(os.path.abspath(self.object_path) + " " + fname + ".in " + fname + ".out " + self.solver_name)
        # read output file
        sans = open(fname + ".out").read().split(" ")
        ans = [(x == "1") for x in sans]
        os.remove(fname + ".in")
        os.remove(fname + ".out")
        if (sans[0] == "UNSAT"):
            return None
        else:
            return ans

