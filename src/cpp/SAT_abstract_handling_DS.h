#ifndef SATHANLDER_H
#define SATHANLDER_H
#include "SAT.h"
#include <vector>
#include <utility>

// an abstract data structure for handling SAT backtracking efficiently
class SATHandlingDS{
    public:
    SATHandlingDS() {}

    // should initializes the ds
    virtual void initialize(int N, std::vector<SATClause> C) = 0;

    // should return the next variable to be interpreted,
    // as well as the value it should be interpreted as first
    // should return NO_NEXT_VAR if all variables are assigned
    virtual std::pair<int,int> next_var(void) = 0;

    // should return the current assignment of the variables
    virtual std::vector<int> current_assignment(void) = 0;

    // updates the assignment of a variable
    virtual void upd_assignment(int curr_var, int value) = 0;

    // rolls back the last variable assignment
    virtual void rollback_assignment(void) = 0;

    // should return whether the current assignment has hope to be extended to a valid one
    virtual bool valid(void) = 0;

    // optional, should return whether to fork the assignment of the current variable
    // receives as input the current number of operating processes
    virtual bool do_fork(int num_processes){
        return false;
    }

};

#endif