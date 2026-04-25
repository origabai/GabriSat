#ifndef PERSISTENT_SEGTREE_H
#define PERSISTENT_SEGTREE_H
#include "SAT.h"
#include "abstract_persistence_dt.h"
#include "backtracking_utils.h"
#include <set>
#include <stack>
#include <utility>
#include <stdexcept>

// a wrapper for multiset that supports rollbacks
// use the issue_ticket() method to get an identifier, and then you can call rollback with that
// ticket, and rollback to that very point. you can also use the undo() method to undo the last change
// be careful when changing elements via reference, as such changes won't affect the rollback functionality
template<class T, T e, bool (*comp)(T, T)>
class PersistentGeneralSegmentTreeDS : public AbstractPersistentDT<std::pair<int, T>>{
    private:
    GeneralSegmentTreeDS<T, e, comp> seg;

    public:
    PersistentGeneralSegmentTreeDS() {}

    void update(int ind, T value) {
        T old_value = seg.get_value(ind);
        this->changes.push(pair<int, T>(ind, old_value));
        seg.update(ind, value);
    }

    pair<int, T> getmin(){
        return seg.getmin();
    }

    // undoes the last change made, and updates changes accordingly
    void undo() override {
        if (this->changes.empty()) {
            throw std::runtime_error("no changes to undo!");
        }
        auto [ind, value] = this->changes.top();
        this->changes.pop();
        seg.update(ind, value);
    }

};

#endif