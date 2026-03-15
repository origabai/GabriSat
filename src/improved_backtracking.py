from math import log2, ceil
from SAT_abstract_backtracker import AbstractBacktrackingSolver
from SAT_abstract_handling_DS import SATHandlingDS

class BetterSATClause:
    def __init__(self, pos_variables: list[int], neg_variables: list[int]):
        self.pos_variables = set(pos_variables)
        self.neg_variables = set(neg_variables)
        self.assigned_pos_variables = set()
        self.assigned_neg_variables = set()
        self.sat = 0 # num of satisfying variables


"""
DS that can support the following operations:
1. update index i to be val
2. return the index with the smallest val
(EVERYTHING IS ZERO INDEXED)
"""
class MinQueryDS:
    # size is one more than the maximum value of an index
    def __init__(self, size):
        self.MAXVAL = int(1e18)
        self.N = 1 << (ceil(log2(size)))
        self.seg = [(i - self.N, self.MAXVAL) for i in range(2 * self.N)]
        for i in range(self.N-1, 0, -1):
            if self.seg[2*i][1] < self.seg[2*i+1][1]:
                self.seg[i] = self.seg[2*i]
            else:
                self.seg[i] = self.seg[2*i+1]
    
    # sets index i to be val
    def update(self, i, val):
        self.seg[i + self.N] = (i, val)
        i += self.N
        i //= 2
        while (i > 0):
            if self.seg[2*i][1] < self.seg[2*i+1][1]:
                self.seg[i] = self.seg[2*i]
            else:
                self.seg[i] = self.seg[2*i+1]
            i //= 2

    # get the index with the minimum val
    def getmin(self):
        return self.seg[1]
        

    
class ImprovedSATHandler(SATHandlingDS):
    def __init__(self, num_variables: int, clauses: list[tuple[list[int],list[int]]]):
        super().__init__(num_variables, clauses)

        # list of all clauses
        self.clause_list : list[BetterSATClause] = []
        for p,n in clauses:
            if len(p) + len(n) > 0:
                self.clause_list.append(BetterSATClause(p, n))
        # current assignment of the variables
        self.assignment : list[bool | None] = [None for i in range(num_variables)]

        # MinQueryDS for this handler
        self.minqryds = MinQueryDS(len(clauses))
        for i in range(len(clauses)):
            p,n = clauses[i]
            self.minqryds.update(i, len(p) + len(n))

        # maps from each variable to indices of all clauses it's in
        self.var_to_clause_map : list[set[int]] = [set() for i in range(self.num_variables)]
        for i in range(len(self.clause_list)):
            for x in self.clause_list[i].neg_variables:
                self.var_to_clause_map[x].add(i)
            for x in self.clause_list[i].pos_variables:
                self.var_to_clause_map[x].add(i)

        # whether the current assignment can be extended
        self.valid_bit = True

        # stack of assigned variables
        self.op_stack = []

    # returns a variable in the clause with the lowest score
    def next_var(self) -> int | None:
        i, v = self.minqryds.getmin()
        if (v == self.minqryds.MAXVAL) or len(self.clause_list[i].pos_variables) + len(self.clause_list[i].neg_variables) == 0:
            # this means everything is already satisfied. give the first unassigned variable
            for i in range(self.num_variables):
                if self.assignment[i] is None:
                    return i
        elif (len(self.clause_list[i].pos_variables) > 0):
            return next(iter(self.clause_list[i].pos_variables))
        else:
            return next(iter(self.clause_list[i].neg_variables))
            


    # returns the current assignment of the variables
    def current_assignment(self) -> list[int]:
        return self.assignment
    

    # updates the assignment of a variable
    def upd_assignment(self, curr_var: int, value: bool):
        # update op stack and assignment
        self.op_stack.append((curr_var, value))
        self.assignment[curr_var] = value
        # go over all clauses containing the current variable(even satisfied ones)
        for cl in self.var_to_clause_map[curr_var]:
            clause = self.clause_list[cl]
            # if a clause is satisifed i don't care about it
            if clause.sat > 0:
                continue
            if value:
                # the clause is now satisifed
                if curr_var in clause.pos_variables:
                    clause.sat += 1
                    clause.pos_variables.remove(curr_var)
                    clause.assigned_pos_variables.add(curr_var)
                    # set it's score to מלאנתלאפים so it doesn't come up in next_var
                    self.minqryds.update(cl, self.minqryds.MAXVAL)
                else: # the clause isn't satisifed immediately
                    # if this is the only variable in the clause, theres a contradiction! save it
                    if (len(clause.neg_variables) + len(clause.pos_variables) == 1):
                        self.valid_bit = False
                    # update everything else
                    clause.neg_variables.remove(curr_var)
                    clause.assigned_neg_variables.add(curr_var)
                    self.minqryds.update(cl, len(clause.pos_variables) + len(clause.neg_variables))
            else: # this is dual to the previous case
                if curr_var in clause.neg_variables:
                    clause.sat += 1
                    clause.neg_variables.remove(curr_var)
                    clause.assigned_neg_variables.add(curr_var)
                    self.minqryds.update(cl, self.minqryds.MAXVAL)
                else:
                    if (len(clause.neg_variables) + len(clause.pos_variables) == 1):
                        self.valid_bit = False
                    clause.pos_variables.remove(curr_var)
                    clause.assigned_pos_variables.add(curr_var)
                    self.minqryds.update(cl, len(clause.pos_variables) + len(clause.neg_variables))



    # rolls back the last variable assignment
    def rollback_assignment(self):
        # pop stack and update assignment
        self.assignment[self.op_stack[-1][0]] = None
        curr_var, value = self.op_stack.pop()
        # the valid bit is always flipped just once, so rollbacking will always set it to True
        self.valid_bit = True
        # go over all clauses the variable is in
        for cl in self.var_to_clause_map[curr_var]:
            clause: BetterSATClause = self.clause_list[cl]
            # this is the case where the clause was already satisfied and we skipped it
            # in this case we don't need to update anything
            if (curr_var not in clause.assigned_neg_variables and curr_var not in clause.assigned_pos_variables):
                continue
            # fix all clauses and rollback the segment tree
            if curr_var in clause.assigned_neg_variables:
                clause.assigned_neg_variables.remove(curr_var)
                clause.neg_variables.add(curr_var)
                self.minqryds.update(cl, len(clause.pos_variables) + len(clause.neg_variables))
                # in the case where the variable was satisfied, update it accordingly
                if not value:
                    clause.sat -=1 
            else:
                clause.assigned_pos_variables.remove(curr_var)
                clause.pos_variables.add(curr_var)
                self.minqryds.update(cl, len(clause.pos_variables) + len(clause.neg_variables))
                if value:
                    clause.sat -= 1
        

    # returns whether the current assignment has hope to be extended to a valid one
    def valid(self) -> bool:
        return self.valid_bit



class ImproverBacktrackingSolver(AbstractBacktrackingSolver):
    def __init__(self, num_variables):
        super().__init__(num_variables, ImprovedSATHandler)

    def solve(self) -> list[int] | None:
        return super().solve()