#ifndef SAT_ABSTRACT_BACKTRACKER_H
#define SAT_ABSTRACT_BACKTRACKER_H

#include "SAT.h"
#include "SAT_abstract_handling_DS.h"
#include "constants.h"
// abstract backtracking solver using the handler DS
class AbstractBacktrackingSolver : public AbstractSATSolver{
    SATHandlingDS *handler;
    public:
    AbstractBacktrackingSolver(int num_variables, SATHandlingDS *ds) : AbstractSATSolver(num_variables), handler(ds) {}

    
    std::vector<int> solve() override {
        handler->initialize(num_variables, clauses);
        return rec_solve();
    }

    std::vector<int> rec_solve() {
        int curr_var = handler->next_var();
        // base case
        if (curr_var == NO_NEXT_VAR){
            return handler->current_assignment();
        }
        // assign true
        handler->upd_assignment(curr_var, SAT_TRUE);
        if (handler->valid()){
            std::vector<int> sol = rec_solve();
            if (sol.size() != 0){
                return sol;
            }
        }
        handler->rollback_assignment();
        
        // assign false
        handler->upd_assignment(curr_var, SAT_FALSE);
        if (handler->valid()){
            std::vector<int> sol = rec_solve();
            if (sol.size() != 0){
                return sol;
            }
        }
        handler->rollback_assignment();
        
        return {};
    }
};

#endif