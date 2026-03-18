"""
this is the python-side endpoint of the cpp-python communication
in order for this to work, add a class inheriting from CPP_SATSolver
to the file cpp_solvers.py
that class's __init__ should set object_path to be the path
of the executable in cpp_executables
see cpp/communication_py.cpp for instructions to create it
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
    as well as a path to an object file implementing the interface
    defined in communication_py.cpp
    """
    def __init__(self, num_variables, object_path):
        super().__init__(num_variables)
        self.object_path = object_path
        
    def solve(self):
        letters = "abcdefghijklmnopqrstuvwxyz"
        # create input file with the correct format
        fname = "".join([choice(letters) for i in range(10)])
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
        os.system(os.path.abspath(self.object_path) + " " + fname + ".in " + fname + ".out")
        # read output file
        sans = open(fname + ".out").read().split(" ")
        ans = [(x == "1") for x in sans]
        os.remove(fname + ".in")
        os.remove(fname + ".out")
        if (len(ans) == 0):
            return None
        else:
            return ans

