from SAT import SATClause, AbstractSATSolver

"""
SAT solver with backtracking
"""


class SAT_backtracking(AbstractSATSolver):
    def __init__(self, num_variables):
        super.__init__(num_variables)

    # returns an array of booleans containing a satisfying solution, or None if impossible
    def solve(self) -> list[int] | None:
        return self.backtrack_solve()

    # backtracking solving of sats. recurses through all interpretations and stops if already wrong
    # returns a list of bools representing the solution if one exists, else None
    def backtrack_solve(self) -> list[bool] | None:
        interpretation: list[bool | None] = [None for _ in range(self.num_variables)]
        # the initial interpretation of the SAT, all starting with None
        unsatisfied: set[int] = set(range(len(self.clauses)))
        # all clauses yet to be satisfied, starting with all clauses
        singelton_clauses: set[tuple[int, bool]] = set()
        # all clauses containing a single element
        for clause_ind, clause in enumerate(self.clauses):
            pos: set[int] = clause.pos_variables
            neg: set[int] = clause.neg_variables
            if len(pos) + len(neg) == 0:  # empty clause
                unsatisfied.remove(clause_ind)
            elif len(pos) + len(neg) == 1:  # singelton_clause
                if len(pos) == 1:
                    singelton_clauses.add(
                        (next(iter(pos)), True)
                    )  # next(iter(.)) is the python way to get an arbitrary element
                else:
                    singelton_clauses.add((next(iter(neg)), False))
        return self.recursive_backtrack_solve(
            interpretation, 0, unsatisfied, singelton_clauses
        )

    # the recursive function that backtrack_solve calls. interpretation is the current interpretation
    # containing True, False or None, with None indicating not selected yet. ind is the index up to
    # we already solved. unsatisfied is a set of ints representing the clauses which are not yet satisfied
    # singelton_clauses is a set of pairs of ints representing the literals who are single in a clause and
    # a bool being True if they are positive literals and False if they are negative literals
    # returns a list of bools representing the solution if one exists, else None
    def recursive_backtrack_solve(
        self,
        interpretation: list[bool | None],
        ind: int,
        unsatisfied: set[int],
        singelton_clauses: set[tuple[int, bool]],
    ) -> list[bool] | None:
        if ind == self.num_variables:  # base case
            return interpretation

        if len(singelton_clauses) > 0:  # there are singelton clauses
            satisfied_clauses: list[int] = []  # needed for undo_literal
            unsatisfied_clauses: list[int] = []  # needed for undo_literal
            new_singeltons: list[tuple[int, bool]] = []  # needed for undo_literal
            literal, value = singelton_clauses.pop()  # try an arbitrary singleton
            if interpretation[literal] == (not value):  # already a contradiction
                singelton_clauses.add((literal, value))  # put it back
                return None
            if interpretation[literal] == value:  # already solved
                solution: list[bool] | None = self.recursive_backtrack_solve(  # recurse
                    interpretation, ind, unsatisfied, singelton_clauses
                )
                singelton_clauses.add((literal, value))  # put it back
                return solution

            check: bool = self.put_in_literal(
                interpretation,
                unsatisfied,
                singelton_clauses,
                literal,
                value,
                satisfied_clauses,
                unsatisfied_clauses,
                new_singeltons,
            )
            if not check:  # there is already a contradiction
                singelton_clauses.add((literal, value))  # put it back
                interpretation[literal] = None
                return None  # impossible since it's a singleton
            solution: list[bool] | None = self.recursive_backtrack_solve(
                interpretation, ind, unsatisfied, singelton_clauses
            )  # continue recursion, we didn't put a value in ind so we use ind instead of ind + 1
            self.undo_literal(
                interpretation,
                unsatisfied,
                singelton_clauses,
                literal,
                value,
                satisfied_clauses,
                unsatisfied_clauses,
                new_singeltons,
            )
            singelton_clauses.add((literal, value))  # put it back
            if solution is None:
                interpretation[literal] = None
            return solution  # might be None, but it's the best thing because we had to satisfy the singleton

        # no singletons so putting values in ind
        if interpretation[ind] is not None:  # if already has a value
            return self.recursive_backtrack_solve(
                interpretation, ind + 1, unsatisfied, singelton_clauses
            )
        for value in [True, False]:
            satisfied_clauses: list[int] = []  # needed for undo_literal
            unsatisfied_clauses: list[int] = []  # needed for undo_literal
            new_singeltons: list[tuple[int, bool]] = []  # needed for undo_literal
            check: bool = self.put_in_literal(
                interpretation,
                unsatisfied,
                singelton_clauses,
                ind,
                value,
                satisfied_clauses,
                unsatisfied_clauses,
                new_singeltons,
            )
            if not check:  # there is already a contradiction
                interpretation[ind] = None
                continue
            solution: list[bool] | None = self.recursive_backtrack_solve(
                interpretation, ind + 1, unsatisfied, singelton_clauses
            )  # continue recursion, we put a value in ind so we use ind + 1
            self.undo_literal(
                interpretation,
                unsatisfied,
                singelton_clauses,
                ind,
                value,
                satisfied_clauses,
                unsatisfied_clauses,
                new_singeltons,
            )
            if solution is not None:  # found solution
                return solution
            interpretation[ind] = None
        interpretation[ind] = None
        return None  # no solution found

    # tries to put value in literal, returns True if successful and you can proceed with recursion,
    # else False. if False was returned you may assume it "cleaned up" after itself and everything is the same.
    # satisfied_clauses, unsatisfied_clauses and new_singeltons should be empty lists, and if True is returned
    # they will contain some ints, they are needed for undoing all of the operations and should be given to undo_literal
    # all other arguments are the same ones as in recursive_backtrack_solve
    def put_in_literal(
        self,
        interpretation: list[bool | None],
        unsatisfied: set[int],
        singelton_clauses: set[tuple[int, bool]],
        literal: int,
        value: bool,
        satisfied_clauses: list[int],
        unsatisfied_clauses: list[int],
        new_singeltons: list[tuple[int, bool]],
    ) -> bool:
        interpretation[literal] = value
        # satisfied_clauses is a list containing the indexes of the clauses that i now satisfies
        # unsatisfied_clauses is a list containing the indexes of the clauses that i now doesn't satisfies
        for clause_ind in unsatisfied:
            clause: SATClause = self.clauses[clause_ind]
            if literal in clause.pos_variables:  # assuming value = True
                satisfied_clauses.append(clause_ind)
            if literal in clause.neg_variables:
                unsatisfied_clauses.append(clause_ind)
        if not value:  # if value is False we have the wrong order
            satisfied_clauses, unsatisfied_clauses = (  # swap
                unsatisfied_clauses,
                satisfied_clauses,
            )
        for clause_ind in satisfied_clauses:
            unsatisfied.remove(clause_ind)
        for loop_ind, clause_ind in enumerate(unsatisfied_clauses):
            clause: SATClause = self.clauses[clause_ind]
            variables: set[int]
            opposite_variables: set[int]
            variables, opposite_variables = (  # assuming value = True
                clause.neg_variables,
                clause.pos_variables,
            )
            if not value:  # literal is actually in pos_variables
                variables, opposite_variables = (
                    opposite_variables,
                    variables,
                )  # swap
            variables.remove(literal)
            if (
                len(variables) + len(opposite_variables) == 0
            ):  # clause now empty, a contradiction
                while len(unsatisfied_clauses) > loop_ind + 1:
                    # removing everything we didn't touch yet leaving only things in need of undoing
                    unsatisfied_clauses.pop()
                self.undo_literal(
                    interpretation,
                    unsatisfied,
                    singelton_clauses,
                    literal,
                    value,
                    satisfied_clauses,
                    unsatisfied_clauses,
                    new_singeltons,
                )
                return False
            # variables is a list and not a set, if large is significantly slower! easy fix
            if (
                len(variables) + len(opposite_variables) == 1
            ):  # clause is now a singelton
                new_literal: int  # the literal in the singelton
                new_value: bool  # the value of the literal in the singelton
                if len(variables) == 1:  # new literal has the same value as literal
                    new_literal = next(iter(variables))
                    new_value = not value
                else:  # new literal has the opposite value from literal
                    new_literal = next(iter(opposite_variables))
                    new_value = value
                if (
                    new_literal,
                    not new_value,
                ) in singelton_clauses:  # we have a contradiction
                    while len(unsatisfied_clauses) > loop_ind + 1:
                        # removing everything we didn't touch yet leaving only things in need of undoing
                        unsatisfied_clauses.pop()
                    self.undo_literal(
                        interpretation,
                        unsatisfied,
                        singelton_clauses,
                        literal,
                        value,
                        satisfied_clauses,
                        unsatisfied_clauses,
                        new_singeltons,
                    )
                    return False
                # checking if already inside, critical for undo_literal
                if (new_literal, new_value) not in singelton_clauses:
                    singelton_clauses.add((new_literal, new_value))
                    # saving the change for undo_literal
                    new_singeltons.append((new_literal, new_value))
        return True  # no contradictions found

    # undoes everything adding a literal does, useful during backtracking
    # should be called after previously calling put_in_literal which returned True
    # arguments are should be the exact same ones previously given to put_in_literal
    def undo_literal(
        self,
        interpretation: list[bool | None],
        unsatisfied: set[int],
        singelton_clauses: set[tuple[int, bool]],
        literal: int,
        value: bool,
        satisfied_clauses: list[int],
        unsatisfied_clauses: list[int],
        new_singeltons: list[tuple[int, bool]],
    ) -> None:
        for singelton in new_singeltons:
            singelton_clauses.remove(singelton)  # removing added singeltons
        for clause_ind in unsatisfied_clauses:
            clause: SATClause = self.clauses[clause_ind]
            variables: set[int] = clause.neg_variables  # assuming value = True
            if not value:  # literal is actually in pos_variables
                variables = clause.pos_variables
            variables.add(literal)
            # variable is a list and not a set, if large is significantly slower! easy fix
        for clause_ind in satisfied_clauses:
            unsatisfied.add(clause_ind)
        satisfied_clauses.clear()
        unsatisfied_clauses.clear()
        new_singeltons.clear()
