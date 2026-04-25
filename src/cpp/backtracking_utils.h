#ifndef BACKTRACKING_UTILS
#define BACKTRACKING_UTILS

#include<functional>
#include "SAT.h"
#include "SAT_abstract_backtracker.h"
#include "SAT_abstract_handling_DS.h"
using std::vector, std::set, std::pair, std::multiset, std::function;

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
2. return the index with the smallest val based on comparator given in template
(EVERYTHING IS ZERO INDEXED)
*/
template<class T, T e, bool (*comp)(T, T)>
class GeneralSegmentTreeDS {
    int N;
    vector<pair<int, T>> seg;
    

    public:

    // size is one more than the maximum value of an index
    GeneralSegmentTreeDS(int size = 0){
        if (size == 0) return;
        N = 1 << (32 - __builtin_clz(size-1)); // don't worry about it
        seg.resize(2*N);
        for (int i=N; i<2*N; i++){
            seg[i] = {i - N, e};
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
    T get_value(int ind) {
        return seg[ind + N];
    }
};

bool lesscomp(int l, int r) {return l < r;}
using MinQueryDS = GeneralSegmentTreeDS<int, minqryds_MAXVAL, lesscomp>;

#endif