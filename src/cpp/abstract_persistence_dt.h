#ifndef PERSISTENT_DT_H
#define PERSISTENT_DT_H
#include "SAT.h"
#include <vector>
#include <stack>
#include <utility>
#include <stdexcept>

// an abstract wrapper for a data structure that supports rollbacks
// has a class S for the elements of the stack used to maintain changes
template<class S>
class AbstractPersistentDT{
    protected:
    // a stack consisting of
    std::stack<S> changes;

    public:
    AbstractPersistentDT() {}

    // returns a "ticket", an identifier used for later rollbacks to tis point
    int issue_ticket() {
        return changes.size();
    }

    // undoes the last change made, and updates changes accordingly
    virtual void undo() {}

    void rollback(int ticket) {
        if (ticket > changes.size()) {
            throw std::invalid_argument("ticket used for rollback is too large!");
        }
        while (ticket < changes.size()) {
            undo(); // undo one change made
        }
    }
};

#endif