#ifndef BACKTRACKING_UTILS
#define BACKTRACKING_UTILS

#include<functional>
#include "SAT.h"
#include "SAT_abstract_backtracker.h"
#include "SAT_abstract_handling_DS.h"
#include "persistent_set.h"
#include <set>
#include <stack>
#include <utility>
using std::vector, std::set, std::pair, std::multiset, std::function;

struct BetterSATClause {
    set<int> pos_variables, neg_variables, assigned_pos_variables, assigned_neg_variables;
    // num of satisfying variables
    int sat = 0;

    BetterSATClause(): pos_variables(set<int>()), neg_variables(set<int>()), assigned_pos_variables(set<int>()), assigned_neg_variables(set<int>()) {}
    
    BetterSATClause(set<int> pos, set<int> neg) : pos_variables(pos), neg_variables(neg), assigned_pos_variables(set<int>()), assigned_neg_variables(set<int>()) {}

    BetterSATClause(SATClause &clause) : pos_variables(clause.pos_variables), neg_variables(clause.neg_variables), assigned_pos_variables(set<int>()), assigned_neg_variables(set<int>()) {}

    int size(){
        return pos_variables.size() + neg_variables.size();
    }
};

struct PersistentSATClause {
    PersistentSet<int> pos_variables, neg_variables;
    // num of satisfying variables
    int sat = 0;

    PersistentSATClause(): pos_variables(PersistentSet<int>()), neg_variables(PersistentSet<int>()) {}
    
    PersistentSATClause(set<int> pos, set<int> neg) : pos_variables(pos), neg_variables(neg) {}

    PersistentSATClause(SATClause &clause) : pos_variables(clause.pos_variables), neg_variables(clause.neg_variables) {}

    int size(){
        return pos_variables.size() + neg_variables.size();
    }
};

/*
DS that can support the following operations:
1. update index i to be val
2. return the index with the smallest val based on comparator given in template
(EVERYTHING IS ZERO INDEXED)
*/
template<class T, T (*e)(), bool (*comp)(T, T)>
class GeneralSegmentTreeDS {
    int N;
    vector<pair<int, T>> seg;
    size_t siz;
    

    public:

    // size is one more than the maximum value of an index
    GeneralSegmentTreeDS(int size = 0) : siz(size) {
        if (size == 0) return;
        N = 1 << (32 - __builtin_clz(size-1)); // don't worry about it
        seg.resize(2*N);
        for (int i=N; i<2*N; i++){
            seg[i] = {i - N, e()};
        }
        for (int i=N-1; i>0; i--){
            if (comp(seg[2 * i].second, seg[2 * i + 1].second)) {
                seg[i] = seg[2 * i];
            }
            else {
                seg[i] = seg[2 * i + 1];
            }
        }
    }

    // sets index i to be val
    void update(int i, T val){
        if (i >= siz) {
            throw std::invalid_argument("index too large!");
        }
        seg[i + N] = pair(i, val);
        i += N;
        i /= 2;
        while (i > 0){
            if (comp(seg[2 * i].second, seg[2 * i + 1].second)) {
                seg[i] = seg[2 * i];
            }
            else {
                seg[i] = seg[2 * i + 1];
            }
            i /= 2;
        }
    }

    // get the min variable (or max or whatever, depends on the implementation)
    pair<int, T> getmin(){
        return seg[1];
    }

    // returns the value at the index (like a vector)
    T get_value(int ind) const {
        return seg[ind + N].second;
    }

    // the size of the data structure
    size_t size() const {
        return siz;
    }
};

struct literal {
    bool has_value = false;
    int pos_clauses = 0, neg_clauses = 0;
    int smallest_pos_clause_size = 1e9, largest_pos_clause_size = 0;
    int smallest_neg_clause_size = 1e9, largest_neg_clause_size = 0;
    int ind = -1;
    literal() {}
    literal(int ind) : ind(ind) {}
    // an element that will always be larger than others
    static literal literal_e() {
        literal e = literal();
        e.has_value = true;
        return e;
    }
    bool operator==(const literal &other) const {
        return this->ind == other.ind;
    }
    void switch_pos_neg() {
        switch(pos_clauses, neg_clauses);
        switch(smallest_pos_clause_size, smallest_neg_clause_size);
        switch(largest_pos_clause_size, largest_neg_clause_size);
    }
};

bool less_literal(literal l1, literal l2) {
    if (l1.has_value) return false;
    if (l2.has_value) return true;
    // if (rand() % 2) return true;
    return true;
}

bool lesscomp(int l, int r) {return l < r;}
int max_val() { return minqryds_MAXVAL; }
using MinQueryDS = GeneralSegmentTreeDS<int, max_val, lesscomp>;

#endif