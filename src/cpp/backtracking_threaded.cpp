#include<iostream>
#include "SAT.h"
#include "SAT_abstract_backtracker.h"
#include "SAT_abstract_handling_DS.h"
#include "backtracking_utils.h" 
#include "twosat_solver.h"
#include "SAT_threaded_backtracker.h"
using std::vector, std::set, std::pair, std::multiset;


class SATHandler_Threaded : public SATHandlingDS{

    int num_variables;
    // list of all clauses
    vector<BetterSATClause> clause_list;
    // current assignment of the variables
    vector<int> assignment;
    // MinQueryDS for this handler
    MinQueryDS minqryds;
    // maps from each variable to indices of all clauses it's in
    vector<set<int>> var_to_clause_map;
    // whether the current assignment can be extended
    bool valid_bit = true;
    // stack of assigned variables
    vector<pair<int,int>> op_stack;
    // set of sizes of the unsatisfied clauses with size > 2
    multiset<int> big_active_clause_sizes;

    public:
    SATHandler_Threaded() {}
    void initialize(int N, std::vector<SATClause> C) override {
        num_variables = N;

        // initialize clauses
        for (SATClause &c : C){
            clause_list.push_back(BetterSATClause(c));
        }
        
        // set all variables to unset
        assignment.assign(N, VARIABLE_UNSET);
        
        // initialize segment tree with the sizes of all clauses
        minqryds = MinQueryDS(clause_list.size());
        for (int i=0; i<clause_list.size(); i++){
            minqryds.update(i, clause_list[i].size());
            if (clause_list[i].size() > 2){
                big_active_clause_sizes.insert(clause_list[i].size());
            }
        }
        
        // for every clause, add it to the map
        // for all variables containing it
        var_to_clause_map.resize(num_variables);
        for (int i=0; i<clause_list.size(); i++){
            for (int x : clause_list[i].neg_variables){
                var_to_clause_map[x].insert(i);
            }
            for (int x : clause_list[i].pos_variables){
                var_to_clause_map[x].insert(i);
            }
        }
    }

    pair<int,int> handle_twosat_case(void){
        TwoSATSolver solver(num_variables);
        for (BetterSATClause &clause : clause_list){
            if (clause.sat) continue;
            solver.addClause(clause.pos_variables, clause.neg_variables);
        }
        for (int i=0; i<num_variables; i++){
            if (assignment[i] == SAT_TRUE){
                solver.addClause({i},{});
            } else if (assignment[i] == SAT_FALSE){
                solver.addClause({},{i});
            }
        }
        vector<int> sol = solver.solve();
        if (sol.size() == 0){
            valid_bit = false;
        } else {
            assignment = sol;
        }
        return {NO_NEXT_VAR, NO_NEXT_VAR};
    }

    // returns a variable in the clause with the lowest score
    pair<int,int> next_var(void) override {
        if (big_active_clause_sizes.size() == 0){
            // solve 2sat instead
            return handle_twosat_case();
        }
        auto [i,v] = minqryds.getmin();
        if ((v == minqryds_MAXVAL) || (clause_list[i].size() == 0)){
            // this means everything is already satisfied. give the first unassigned variable
            for (int i=0; i<num_variables; i++){
                if (assignment[i] == VARIABLE_UNSET){
                    return {i,SAT_TRUE};
                }
            }
        } else if (clause_list[i].pos_variables.size() > 0){
            return {*clause_list[i].pos_variables.begin(), SAT_TRUE};
        } else {
            return {*clause_list[i].neg_variables.begin(), SAT_FALSE};
        }
        return {NO_NEXT_VAR, NO_NEXT_VAR};
    }

    std::vector<int> current_assignment(void) override {
        return assignment;
    }

    void upd_assignment(int curr_var, int value) override {
        // update op stack and assignment
        op_stack.push_back({curr_var, value});
        assignment[curr_var] = value;
        // go over all clauses containing the current variable(even satisfied ones)
        for (int cl : var_to_clause_map[curr_var]){
            BetterSATClause &clause = clause_list[cl];
            // if a clause is satisifed i don't care about it
            if (clause.sat > 0){
                continue;
            }
            std::cout << getpid() << " " << __LINE__ << std::endl;
            if (value == SAT_TRUE){
                if (clause.pos_variables.count(curr_var)){
                    // the clause is now satisfied
                    if (clause.size() > 2){
                        big_active_clause_sizes.erase(big_active_clause_sizes.find(clause.size()));
                    }
                    clause.sat++;
                    clause.pos_variables.erase(curr_var);
                    clause.assigned_pos_variables.insert(curr_var);
                    // set it's score to מלאנתלאפים so it doesn't come up in next_var
                    minqryds.update(cl, minqryds_MAXVAL);
                } else {
                    // the clause isn't satisifed immediately
                    // if this is the only variable in the clause, theres a contradiction! save it
                    if (clause.size() == 1){
                        valid_bit = false;
                    }
                    // update everything else
                    if (clause.size() > 2){
                        big_active_clause_sizes.erase(big_active_clause_sizes.find(clause.size()));
                    }
                    clause.neg_variables.erase(curr_var);
                    clause.assigned_neg_variables.insert(curr_var);
                    minqryds.update(cl, clause.size());
                    if (clause.size() > 2){
                        big_active_clause_sizes.insert(clause.size());
                    }
                }
            } else {
                // this is dual to the previous case
                if (clause.neg_variables.count(curr_var)){
                    if (clause.size() > 2){
                        big_active_clause_sizes.erase(big_active_clause_sizes.find(clause.size()));
                    }
                    clause.sat++;
                    clause.neg_variables.erase(curr_var);
                    clause.assigned_neg_variables.insert(curr_var);
                    minqryds.update(cl, minqryds_MAXVAL);
                } else {
                    if (clause.size() == 1){
                        valid_bit = false;
                    }
                    if (clause.size() > 2){
                        big_active_clause_sizes.erase(big_active_clause_sizes.find(clause.size()));
                    }
                    clause.pos_variables.erase(curr_var);
                    clause.assigned_pos_variables.insert(curr_var);
                    minqryds.update(cl, clause.size());
                    if (clause.size() > 2){
                        big_active_clause_sizes.insert(clause.size());
                    }
                }
            }
        }
    }

    // rolls back the last variable assignment
    void rollback_assignment(void) override {
        // pop stack and update assignment
        assignment[op_stack.back().first] = VARIABLE_UNSET;
        auto [curr_var, value] = op_stack.back();
        op_stack.pop_back();
        // the valid bit is always flipped just once, so rollbacking will always set it to True
        valid_bit = true;
        // go over all clauses the variable is in
        for (int cl : var_to_clause_map[curr_var]){
            BetterSATClause &clause = clause_list[cl];
            // this is the case where the clause was already satisfied and we skipped it
            // in this case we don't need to update anything
            if (clause.assigned_neg_variables.count(curr_var) == 0 && clause.assigned_pos_variables.count(curr_var) == 0){
                continue;
            }
            // fix all clauses and rollback the segment tree
            if (clause.assigned_neg_variables.count(curr_var)){
                // if the clause is unsatisfied WITH the variable, erase
                if (clause.sat == 0){
                    if (clause.size() > 2) big_active_clause_sizes.erase(big_active_clause_sizes.find(clause.size()));  
                }
                clause.assigned_neg_variables.erase(curr_var);
                clause.neg_variables.insert(curr_var);
                minqryds.update(cl, clause.size());
                // in the case where the variable was satisfied, update it accordingly
                if (value == SAT_FALSE){
                    clause.sat--;
                }
                if (clause.size() > 2) big_active_clause_sizes.insert(clause.size());
            } else {
                if (clause.sat == 0){
                    if (clause.size() > 2) big_active_clause_sizes.erase(big_active_clause_sizes.find(clause.size()));  
                }
                clause.assigned_pos_variables.erase(curr_var);
                clause.pos_variables.insert(curr_var);
                minqryds.update(cl, clause.size());
                if (value == SAT_TRUE){
                    clause.sat--;
                }
                if (clause.size() > 2) big_active_clause_sizes.insert(clause.size());
            }
        }
    }

    // returns whether the current assignment has hope to be extended to a valid one
    bool valid(void) override {
        return valid_bit;
    }

    bool do_fork(int num_processes) override{
        return (num_processes < MAX_PROCESSES);
        // return false;
    }
};

class ThreadedSolver : public AbstractThreadedSolver {
    public:
    ThreadedSolver(int num_variables) : AbstractThreadedSolver(num_variables, new SATHandler_Threaded()) {}
};