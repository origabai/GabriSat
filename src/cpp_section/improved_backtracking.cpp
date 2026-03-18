#include "SAT.h"
#include "SAT_abstract_backtracker.h"
#include "SAT_abstract_handling_DS.h"
using std::vector, std::set, std::pair;

struct BetterSATClause {
    set<int> pos_variables, neg_variables, assigned_pos_variables, assigned_neg_variables;
    // num of satisfying variables
    int sat = 0;
    BetterSATClause(set<int> pos, set<int> neg) : pos_variables(pos), neg_variables(neg), assigned_pos_variables(set<int>()), assigned_neg_variables(set<int>()) {}

    BetterSATClause(SATClause &clause) : pos_variables(clause.pos_variables), neg_variables(clause.neg_variables), assigned_pos_variables(set<int>()), assigned_neg_variables(set<int>()) {}

    int size(){
        return pos_variables.size() + neg_variables.size();
    }
};

/*
DS that can support the following operations:
1. update index i to be val
2. return the index with the smallest val
(EVERYTHING IS ZERO INDEXED)
*/
class MinQueryDS {
    int N;
    vector<pair<int,int>> seg;
    

    public:

    // size is one more than the maximum value of an index
    MinQueryDS(int size = 0){
        if (size == 0) return;
        N = 1 << (32 - __builtin_clz(size-1)); // don't worry about it
        seg.resize(2*N);
        for (int i=N;i<2*N;i++){
            seg[i] = {i - N, minqryds_MAXVAL};
        }
        for (int i=N-1;i>0;i--){
            if (seg[2*i].second < seg[2*i+1].second){
                seg[i] = seg[2*i];
            } else {
                seg[i] = seg[2*i+1];
            }
        }
    }

    // sets index i to be val
    void update(int i, int val){
        seg[i + N] = {i, val};
        i += N;
        i /= 2;
        while (i > 0){
            if (seg[2*i].second < seg[2*i+1].second){
                seg[i] = seg[2*i];
            } else {
                seg[i] = seg[2*i+1];
            }
            i /= 2;
        }
    }

    // get the index and val with the minimum val
    pair<int,int> getmin(){
        return seg[1];
    }
};

class ImprovedSATHandler : public SATHandlingDS{

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

    public:
    ImprovedSATHandler() {}
    void initialize(int N, std::vector<SATClause> C) override {
        num_variables = N;

        for (auto &c : C){
            clause_list.push_back(BetterSATClause(c));
        }
        
        assignment.assign(N, VARIABLE_UNSET);
        
        minqryds = MinQueryDS(clause_list.size());
        for (int i=0;i<clause_list.size();i++){
            minqryds.update(i, clause_list[i].size());
        }
        
        var_to_clause_map.resize(num_variables);
        for (int i=0;i<clause_list.size();i++){
            for (int x : clause_list[i].neg_variables){
                var_to_clause_map[x].insert(i);
            }
            for (int x : clause_list[i].pos_variables){
                var_to_clause_map[x].insert(i);
            }
        }
    }

    // returns a variable in the clause with the lowest score
    int next_var(void) override {
        auto [i,v] = minqryds.getmin();
        if ((v == minqryds_MAXVAL) || (clause_list[i].size() == 0)){
            // this means everything is already satisfied. give the first unassigned variable
            for (int i=0;i<num_variables;i++){
                if (assignment[i] == VARIABLE_UNSET){
                    return i;
                }
            }
        } else if (clause_list[i].pos_variables.size() > 0){
            return *clause_list[i].pos_variables.begin();
        } else {
            return *clause_list[i].neg_variables.begin();
        }
        return NO_NEXT_VAR;
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
            if (value == SAT_TRUE){
                if (clause.pos_variables.count(curr_var)){
                    // the clause is now satisfied
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
                    clause.neg_variables.erase(curr_var);
                    clause.assigned_neg_variables.insert(curr_var);
                    minqryds.update(cl, clause.size());
                }
            } else {
                // this is dual to the previous case
                if (clause.neg_variables.count(curr_var)){
                    clause.sat++;
                    clause.neg_variables.erase(curr_var);
                    clause.assigned_neg_variables.insert(curr_var);
                    minqryds.update(cl, minqryds_MAXVAL);
                } else {
                    if (clause.size() == 1){
                        valid_bit = true;
                    }
                    clause.pos_variables.erase(curr_var);
                    clause.assigned_pos_variables.insert(curr_var);
                    minqryds.update(cl, clause.size());
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
                clause.assigned_neg_variables.erase(curr_var);
                clause.neg_variables.insert(curr_var);
                minqryds.update(cl, clause.size());
                // in the case where the variable was satisfied, update it accordingly
                if (value == SAT_FALSE){
                    clause.sat--;
                }
            } else {
                clause.assigned_pos_variables.erase(curr_var);
                clause.pos_variables.insert(curr_var);
                minqryds.update(cl, clause.size());
                if (value == SAT_TRUE){
                    clause.sat--;
                }
            }
        }
    }

    // returns whether the current assignment has hope to be extended to a valid one
    bool valid(void) override {
        return valid_bit;
    }
};

class ImproverBacktrackingSolver : public AbstractBacktrackingSolver {
    public:
    ImproverBacktrackingSolver(int num_variables) : AbstractBacktrackingSolver(num_variables, new ImprovedSATHandler()) {}
};