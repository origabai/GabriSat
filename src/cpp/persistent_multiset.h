#ifndef PERSISTENT_ MULTISET_H
#define PERSISTENT_MULTISET_H
#include "SAT.h"
#include "abstract_persistence_dt.h"
#include <set>
#include <stack>
#include <utility>
#include <stdexcept>

// a wrapper for multiset that supports rollbacks
// use the issue_ticket() method to get an identifier, and then you can call rollback with that
// ticket, and rollback to that very point. you can also use the undo() method to undo the last change
// be careful when changing elements via reference, as such changes won't affect the rollback functionality
template<class T>
class PersistentMultiset : public AbstractPersistentDT<std::pair<bool, T>>{
    private:
    std::multiset<T> st;

    public:
    PersistentMultiset() {}

    template <typename... Args>// cpp dark python like magic
    auto insert(Args&&... args) {
        // still black magic, forwarding the arguments
        auto res = st.insert(std::forward<Args>(args)...);
        // always inserted, true for inserting, res.first is the element added
        this->changes.push(pair<bool, int>(true, res.first));
        return res;// forwarding the return value
    }

    size_t erase(const T& value) { // erase by value
        int count = st.count(value);
        size_t res = st.erase(value);
        for (int i = 0; i < count; ++i) {// one for each removal
            // false for erasing
            this->changes.push(pair<bool, int>(false, value));
        }
        return res;// forwarding the return value
    }

    auto erase(typename std::set<T>::iterator it) { // erase by iterator
        T value = *it; // a copy because we will erase it
        auto nextIt = data.erase(it);
        // false for erasing
        this->changes.push(pair<bool, int>(false, value));
        return nextIt;
    }

    // undoes the last change made, and updates changes accordingly
    void undo() override {
        if (this->changes.empty()) {
            throw std::runtime_error("set is empty! nothing to undo!");
        }
        auto [is_insert, value] = this->changes.top();
        this->changes.pop();
        if (is_insert) {
            st.erase(st.find(value));// opposite of inserting is erasing (only one)
        }
        else {
            st.insert(value);// opposite of erasing is inserting
        }
    }

    size_t size() { return vec.size(); }

    bool empty() { return st.empty(); }

    auto begin() { return st.begin(); }

    auto end() { return st.end(); }

    auto find(T& key) { return st.find(key); }

    auto count(T& key) { return st.count(key); }
    
    auto contains(T& key) { return st.contains(key); }

    auto lower_bound(T& key) { return st.lower_bound(key); }
    
    auto upper_bound(T& key) { return st.upper_bound(key); }
};

#endif