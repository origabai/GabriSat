#include "SAT.h"
#include "SAT_abstract_backtracker.h"
#include "SAT_abstract_handling_DS.h"
#include "backtracking_utils.h" 
#include "twosat_solver.h"
#include "persistent_vector.h"
#include "persistent_set.h"
#include "persistent_multiset.h"
#include "persistent_segment_tree.h"
#include "SAT_threaded_backtracker.h"
#include <iostream>
using std::vector, std::set, std::pair, std::multiset;

class SATHandler_Hamcycle : public SATHandlingDS{
    // is there a contradiction in the whole SAT from the beginning
    bool empty_clause = false;
    int num_variables;
    // list of all clauses
    vector<PersistentSATClause> clause_list;
    // current assignment of the variables
    PersistentVector<int> assignment;
    // MinQueryDS for this handler
    PersistentGeneralSegmentTreeDS<literal, literal::literal_e, less_literal> minqryds;
    // maps from each variable to indices of all unsatisfied positive \ negative clauses it's in, first is the clause current size,
    // second is the clause index. note that a positive clause means that this specific variable needs to be true to satisfy it and vice versa
    vector<PersistentSet<pair<int, int>>> var_to_pos_clause_map, var_to_neg_clause_map;
    // a vector of bools denoting if a var_to_clause_map at some index have been changed
    // note: this isn't used like other persistent ds, but at each recursive step it "cleans itself",
    // so do not add it to persistent_data_structures, it's not a bug, it's a feature!
    // one is for var_to_pos_clause_map and one for var_to_neg_clause_map
    PersistentVector<bool> pos_set_updated, neg_set_updated;
    // the ticket used to always rollback set_updated to the same starting point
    const int set_updated_ticket = 0;
    // whether the current assignment can be extended
    bool valid_bit = true;
    // stack of assigned variables
    // vector<pair<int,int>> op_stack;
    // a multiset containing all sizes of active clauses, used to check if we can solve a 2SAT instead
    PersistentMultiset<int> active_clause_sizes;
    // a stack of vectors of pointers to all of the persistent data structures that need to be updated,
    // denoting which ticket refers to which ds
    stack<vector<PersistentInterface*>> persistent_data_structures_stack;
    // a stack of vectors of numbers, used to save the rollback tickets at each recursive step
    stack<vector<int>> tickets;
    // a list of all persistent data structures that need to be saved at each recursive step
    vector<PersistentInterface*> persistent_data_structures = {
        (PersistentInterface*)(&assignment),
        (PersistentInterface*)(&minqryds),
        (PersistentInterface*)(&active_clause_sizes)
    };

    public:
    SATHandler_Hamcycle() {}
    void initialize(int N, std::vector<SATClause> C) override {
        num_variables = N;

        // initialize clauses
        // clause_list = vector<PersistentSATClause>(C.size());
        for (int i = 0; i < C.size(); ++i) {
            if (C[i].pos_variables.size() + C[i].neg_variables.size() == 0) {// if clause is empty
                empty_clause = true;
            }
            // checking if a clause contains a variable as both pos and neg
            bool stupid_clause = false;
            for (int var : C[i].pos_variables) {
                if (C[i].neg_variables.count(var)) {
                    stupid_clause = true;
                }
            }
            if (!stupid_clause) clause_list.push_back(PersistentSATClause(C[i]));
        }

        // set all variables to unset
        assignment = PersistentVector<int>(N, VARIABLE_UNSET);
        
        // initialise minqueryds
        minqryds = PersistentGeneralSegmentTreeDS<literal, literal::literal_e, less_literal>(num_variables);

        // initialize to all false
        pos_set_updated = PersistentVector<bool>(num_variables, false);
        neg_set_updated = PersistentVector<bool>(num_variables, false);
        
        // for every clause, add it to the map for all variables containing it, while updating the minqueryds
        var_to_pos_clause_map.resize(num_variables);
        var_to_neg_clause_map.resize(num_variables);
        
        // initialising the map from variables to pos/neg clauses they're in, and active_clause_sizes
        for (int i=0; i<clause_list.size(); i++){
            for (int x : clause_list[i].neg_variables){
                var_to_neg_clause_map[x].insert({clause_list[i].size(), i});
            }
            for (int x : clause_list[i].pos_variables){
                var_to_pos_clause_map[x].insert({clause_list[i].size(), i});
            }
            active_clause_sizes.insert(clause_list[i].size());
        }

        // initialising minqueryds for all variables
        for (int var = 0; var < num_variables; var++) {
            literal l(var);
            l.has_value = false;
            l.smallest_pos_clause_size = get_set_min_else(var_to_pos_clause_map[var], 1e9);
            l.largest_pos_clause_size = get_set_max_else(var_to_pos_clause_map[var], 0);
            l.smallest_neg_clause_size = get_set_min_else(var_to_neg_clause_map[var], 1e9);
            l.largest_neg_clause_size = get_set_max_else(var_to_neg_clause_map[var], 0);
            l.pos_clauses = var_to_pos_clause_map[var].size();
            l.neg_clauses = var_to_neg_clause_map[var].size();
            minqryds.update(var, l);
        }
    }

    // called when in a 2SAT, it solves it via a 2SAT solver, 
    pair<int,int> handle_twosat_case(void){
        TwoSATSolver solver(num_variables);
        for (PersistentSATClause &clause : clause_list){
            if (clause.sat[0]) continue;
            solver.addClause(set<int>(clause.pos_variables), set<int>(clause.neg_variables));
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
            assignment = PersistentVector<int>(sol);
        }
        return {NO_NEXT_VAR, NO_NEXT_VAR};
    }

    // returns a variable in the clause with the lowest score
    pair<int,int> next_var(void) override {
        // if you want do disable solving 2SAT with a 2SAT solver you can just comment out the following 3 lines
        if (*active_clause_sizes.rbegin() <= 2) { // largest unsatisfied clause is at size at most 2
            return handle_twosat_case(); // solve a 2SAT instead
        }
        auto [i,v] = minqryds.getmin(); // the chosen literal var
        if ((v == literal::literal_e()) || v.has_value) {
            return {NO_NEXT_VAR, NO_NEXT_VAR};
        }
        return {i, choose_truth_val(i, v)};
    }

    std::vector<int> current_assignment(void) override {
        return assignment;
    }

    void upd_assignment(int curr_var, int value) override {
        // erase all of pos_set_updated and neg_set_updated
        pos_set_updated.rollback(set_updated_ticket);
        neg_set_updated.rollback(set_updated_ticket);

        
        // taking a ticket for all persistent data structures
        issue_tickets(); 

        // update op stack and assignment
        // op_stack.push_back({curr_var, value});
        assignment[curr_var] = value;

        if (empty_clause) { // if there was a contradiction from the start
            valid_bit = false;
            return;
        }


        // save that now curr_var has a value so we don't choose it in the future
        literal new_value = minqryds.get_value(curr_var);
        new_value.has_value = true;
        minqryds.update(curr_var, new_value);


        // go over all unsatisfied clauses containing the current variable that it satisfies
        {
            vector<PersistentSet<pair<int, int>>> &var_to_clause_map = (value == SAT_TRUE) ? var_to_pos_clause_map : var_to_neg_clause_map;
            for (auto[clause_size, clause_ind] : vector<pair<int, int>>(var_to_clause_map[curr_var])) { // casting to a vector so we can delete elements and not worry about it
                if (clause_list[clause_ind].sat[0]) { // clause already satisfied
                    continue;
                }

                // the clause is now satisfied
                tickets.top().push_back(clause_list[clause_ind].sat.issue_ticket());
                persistent_data_structures_stack.top().push_back((PersistentInterface*)(&clause_list[clause_ind].sat));
                clause_list[clause_ind].sat[0] = 1;

                // erasing it's size from active_clause_sizes
                active_clause_sizes.erase(active_clause_sizes.find(clause_size));
                
                // update all positive variables in the clause
                for (int var : clause_list[clause_ind].pos_variables) {
                    if (var == curr_var) continue;
                    set_erase(var, true, pair<int, int>(clause_size, clause_ind));
                    literal new_value = minqryds.get_value(var);
                    new_value.smallest_pos_clause_size = get_set_min_else(var_to_pos_clause_map[var], 1e9);
                    new_value.largest_pos_clause_size = get_set_max_else(var_to_pos_clause_map[var], 0);
                    new_value.pos_clauses--;
                    minqryds.update(var, new_value);
                }

                // now the negative variables of the clause
                for (int var : clause_list[clause_ind].neg_variables) {
                    if (var == curr_var) continue;
                    set_erase(var, false, pair<int, int>(clause_size, clause_ind));
                    literal new_value = minqryds.get_value(var);
                    new_value.smallest_neg_clause_size = get_set_min_else(var_to_neg_clause_map[var], 1e9);
                    new_value.largest_neg_clause_size = get_set_max_else(var_to_neg_clause_map[var], 0);
                    new_value.neg_clauses--;
                    minqryds.update(var, new_value);
                }
            }
        }

        // now the second case 
        // go over all unsatisfied clauses containing the current variable that it doesn't satisfies
        {
            vector<PersistentSet<pair<int, int>>> &var_to_clause_map = (value == SAT_FALSE) ? var_to_pos_clause_map : var_to_neg_clause_map;
            bool pos = (value == SAT_FALSE);
            for (auto[clause_size, clause_ind] : vector<pair<int, int>>(var_to_clause_map[curr_var])) { // casting to a vector so we can delete elements and not worry about it
                if (clause_list[clause_ind].sat[0]) { // clause already satisfied
                    continue;
                }

                // the clause is still unsatisfied

                // erasing it's size from active_clause_sizes
                active_clause_sizes.erase(active_clause_sizes.find(clause_size));

                // new size of the clause
                clause_size--;
                if (clause_size == 0) { // found a contradiction
                    valid_bit = false;
                    return;
                }

                // inserting the new size
                active_clause_sizes.insert(clause_size);

                // erasing curr_var from this clause, wasn't needed in the second case because the
                // clause was already satisfied
                if (pos) { // curr_varr is positive in this clause
                    // before changing the clause set take a ticket to save it's state
                    this->tickets.top().push_back(clause_list[clause_ind].pos_variables.issue_ticket());
                    this->persistent_data_structures_stack.top().push_back((PersistentInterface*)(&(clause_list[clause_ind].pos_variables)));
                    // now we can erase curr_var with no worries
                    clause_list[clause_ind].pos_variables.erase(curr_var);
                }
                else {// curr_varr is negative in this clause
                    // before changing the clause set take a ticket to save it's state
                    this->tickets.top().push_back(clause_list[clause_ind].neg_variables.issue_ticket());
                    this->persistent_data_structures_stack.top().push_back((PersistentInterface*)(&(clause_list[clause_ind].neg_variables)));
                    // now we can erase curr_var with no worries
                    clause_list[clause_ind].neg_variables.erase(curr_var);
                }

                // starting with the positive variables of the clause
                
                for (int var : clause_list[clause_ind].pos_variables) {
                    if (var == curr_var) continue;
                    set_erase(var, true, pair<int, int>(clause_size + 1, clause_ind));
                    set_insert(var, true, pair<int, int>(clause_size, clause_ind));
                    literal new_value = minqryds.get_value(var);
                    new_value.smallest_pos_clause_size = get_set_min_else(var_to_pos_clause_map[var], 1e9);
                    new_value.largest_pos_clause_size = get_set_max_else(var_to_pos_clause_map[var], 0);
                    minqryds.update(var, new_value);
                }

                // now the negative variables of the clause
                for (int var : clause_list[clause_ind].neg_variables) {
                    if (var == curr_var) continue;
                    set_erase(var, false, pair<int, int>(clause_size + 1, clause_ind));
                    set_insert(var, false, pair<int, int>(clause_size, clause_ind));
                    literal new_value = minqryds.get_value(var);
                    new_value.smallest_neg_clause_size = get_set_min_else(var_to_neg_clause_map[var], 1e9);
                    new_value.largest_neg_clause_size = get_set_max_else(var_to_neg_clause_map[var], 0);
                    minqryds.update(var, new_value);
                }
            }
        }
    }

    // rolls back the last variable assignment
    void rollback_assignment(void) override {
        // the valid bit is always flipped just once, so rollbacking will always set it to True
        valid_bit = true;
        rollback_ds();// rollbacks all of the persistent ds changed
    }

    // returns whether the current assignment has hope to be extended to a valid one
    bool valid(void) override {
        return valid_bit;
    }

    virtual pair<int,int> fork_variable(int num_processes){
        if (num_processes >= MAX_PROCESSES) return {NO_NEXT_VAR, NO_NEXT_VAR};
        if (*active_clause_sizes.rbegin() <= 2){
            // solve 2sat instead
            return {NO_NEXT_VAR, NO_NEXT_VAR};
        }
        auto [i1, l1] = minqryds.getmin();
        if (l1.has_value) return {NO_NEXT_VAR, NO_NEXT_VAR};
        int i2 = -1;
        for (int i = 0; i < 10; ++i) {
            i2 = rand() % num_variables;
            if (!minqryds.get_value(i2).has_value) break;
        }
        if (!minqryds.get_value(i2).has_value) {
            return {i1, i2};
        }
        return { NO_NEXT_VAR, NO_NEXT_VAR };
    }

    // issues rollback tickets for all ds in persistent_data_structures, later used for rollbacks
    void issue_tickets() {
        int n = this->persistent_data_structures.size();
        vector<int> ticket_vec(n);
        for (int i = 0; i < n; ++i) {
            ticket_vec[i] = this->persistent_data_structures[i]->issue_ticket();
        }
        this->tickets.push(ticket_vec);
        this->persistent_data_structures_stack.push(this->persistent_data_structures);
    }

    // performs a rollback of all ds in persistent_data_structures up to the last time issue tickets has been performed
    // be carefull to issue tickets at every recursive step, and to rollback at each return point. also do not perform
    // rollbacks manually on ds in persistent_data_structures as it may interfere with this functionality
    void rollback_ds() {
        vector<int> ticket_vec = this->tickets.top();
        this->tickets.pop();
        vector<PersistentInterface*> data_structures = this->persistent_data_structures_stack.top();
        this->persistent_data_structures_stack.pop();
        int n = data_structures.size();
        for (int i = 0; i < n; ++i) {
            data_structures[i]->rollback(ticket_vec[i]);
        }
    }


    // used to insert a value to one of var_to_pos_clause_map, var_to_neg_clause_map in a way that updates the rollback
    // so that you don't need to worry about it at all.
    // called when you want to insert element e into ind index of the pos \ neg variant of var_to_pos_clause_map, where
    // a pos = true value denotes the pos variant, and pos = false denotes the neg variant
    void set_insert(int ind, bool pos, pair<int, int> e) {
        if (pos) {// pos case
            if (!pos_set_updated[ind]) {
                pos_set_updated[ind] = true;
                this->persistent_data_structures_stack.top().push_back((PersistentInterface*)&var_to_pos_clause_map[ind]);
                this->tickets.top().push_back(var_to_pos_clause_map[ind].issue_ticket());
            }
            var_to_pos_clause_map[ind].insert(e);
        }
        else {// neg case
            if (!neg_set_updated[ind]) {
                neg_set_updated[ind] = true;
                this->persistent_data_structures_stack.top().push_back((PersistentInterface*)&var_to_neg_clause_map[ind]);
                this->tickets.top().push_back(var_to_neg_clause_map[ind].issue_ticket());
            }
            var_to_neg_clause_map[ind].insert(e);
        }
    }

    
    // used to erase a value from one of var_to_pos_clause_map, var_to_neg_clause_map in a way that updates the rollback
    // so that you don't need to worry about it at all.
    // called when you want to erase element e from ind index of the pos \ neg variant of var_to_pos_clause_map, where
    // a pos = true value denotes the pos variant, and pos = false denotes the neg variant
    void set_erase(int ind, bool pos, pair<int, int> e) {
        if (pos) {// pos case
            if (!pos_set_updated[ind]) {
                pos_set_updated[ind] = true;
                this->persistent_data_structures_stack.top().push_back((PersistentInterface*)&var_to_pos_clause_map[ind]);
                this->tickets.top().push_back(var_to_pos_clause_map[ind].issue_ticket());
            }
            var_to_pos_clause_map[ind].erase(e);
        }
        else {// neg case
            if (!neg_set_updated[ind]) {
                neg_set_updated[ind] = true;
                this->persistent_data_structures_stack.top().push_back((PersistentInterface*)&var_to_neg_clause_map[ind]);
                this->tickets.top().push_back(var_to_neg_clause_map[ind].issue_ticket());
            }
            var_to_neg_clause_map[ind].erase(e);
        }
    }

    // a major part of the heuristic, given some chosen literal, which truth value do we want to try first
    // should always return one of { SAT_FALSE, SAT_TRUE }
    int choose_truth_val(int ind, literal l) {
        if (l.smallest_neg_clause_size == 1) return SAT_FALSE;
        if (l.smallest_pos_clause_size == 1) return SAT_TRUE;
        if (l.pos_clauses == 0) return SAT_FALSE;
        if (l.neg_clauses == 0) return SAT_TRUE;
        // do not change, all of this is necessary regardless of heuristic

        int r = rand() % (l.pos_clauses + l.neg_clauses);
        if (r < l.pos_clauses) return SAT_TRUE;
        return SAT_FALSE;
    }

    int get_set_min_else(PersistentSet<pair<int, int>>& s, int e) {
        if (!s.size()) {
            return e;
        }
        return (*s.begin()).first;
    }

    int get_set_max_else(PersistentSet<pair<int, int>>& s, int e) {
        if (!s.size()) {
            return e;
        }
        return (*s.rbegin()).first;
    }
};

class HamcycleSolver : public AbstractThreadedSolver {
    public:
    HamcycleSolver(int num_variables) : AbstractThreadedSolver(num_variables, new SATHandler_Hamcycle()) {}
};