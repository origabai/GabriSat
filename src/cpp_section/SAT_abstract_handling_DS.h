#ifndef SATHANLDER_H
#define SATHANLDER_H
#include "SAT.h"
#include <vector>

// an abstract data structure for handling SAT backtracking efficiently
class SATHandlingDS{
    public:
    SATHandlingDS() {}

    // should initializes the ds
    virtual void initialize(int N, std::vector<SATClause> C) = 0;

    // should return the next variable to be interpreted
    // should return NO_NEXT_VAR if all variables are assigned
    virtual int next_var(void) = 0;

    // should return the current assignment of the variables
    virtual std::vector<int> current_assignment(void) = 0;

    // updates the assignment of a variable
    virtual void upd_assignment(int curr_var, int value) = 0;

    // rolls back the last variable assignment
    virtual void rollback_assignment(void) = 0;

    // should return whether the current assignment has hope to be extended to a valid one
    virtual bool valid(void) = 0;

};

#endif