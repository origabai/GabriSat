#ifndef BACKTRACKING_UTILS
#define BACKTRACKING_UTILS

#include "SAT.h"
#include "SAT_abstract_backtracker.h"
#include "SAT_abstract_handling_DS.h"
using std::vector, std::set, std::pair, std::multiset;

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

#endif