# a general template for a sat reducible problem. all problems should inherit from this class.
class SATReducibleProblem:
    def __init__(self):
        pass

    # should return a random instance of the problem, ideally an interesting one.
    @classmethod
    def generate(self, size: int):
        pass

    # should return a solution to the problem, or None otherwise
    def solve(self):
        pass