#ifndef SAT_H
#define SAT_H
#include<vector>
#include<set>

struct SATClause {
    std::set<int> pos_variables;
    std::set<int> neg_variables;
    SATClause(std::set<int> pos, std::set<int> neg) : pos_variables(pos), neg_variables(neg) {}
};

class AbstractSATSolver {
    protected:
    int num_variables;
    std::vector<SATClause> clauses;

    public:
    AbstractSATSolver(int num_variables) : num_variables(num_variables){}

    void addClause(std::set<int> pos, std::set<int> neg){
        clauses.push_back(SATClause(pos, neg));
    }

    // should solve the SAT.
    // should return NO_SOLUTION if no solution exists
    virtual std::vector<int> solve() = 0;

};
#endif