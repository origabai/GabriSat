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
        auto [curr_var, truthval] = handler->next_var();
        // base case
        if (curr_var == NO_NEXT_VAR){
            if (handler->valid()) return handler->current_assignment();
            else return {};
        }
        // assigns suggested value
        handler->upd_assignment(curr_var, truthval);
        if (handler->valid()){
            std::vector<int> sol = rec_solve();
            if (sol.size() != 0){
                return sol;
            }
        }
        handler->rollback_assignment();
        
        // assign opposite
        if (truthval == SAT_TRUE){
            truthval = SAT_FALSE;
        } else {
            truthval = SAT_TRUE;
        }
        handler->upd_assignment(curr_var, truthval);
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