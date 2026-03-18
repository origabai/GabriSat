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

    def addClause(self, pos_variables, neg_variables):
        return super().addClause(pos_variables, neg_variables)
        
    def solve(self):
        letters = "abcdefghijklmnopqrstuvwxyz"
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
        os.system(self.object_path + " " + fname + ".in " + fname + ".out")
        sans = open(fname + ".out").read().split(" ")
        ans = [(x == 1) for x in sans]
        # os.remove(fname + ".in")
        # os.remove(fname + ".out")
        return ans

def main():
    solver = CPP_SATSolver(5, "improved_backtracker.exe")
    solver.addClause([1,2],[])
    solver.addClause([3],[1])
    solver.addClause([4],[2])
    print(solver.solve())

if __name__ == "__main__":
    main()