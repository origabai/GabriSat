#ifndef PERSISTENT_SET_H
#define PERSISTENT_SET_H
#include "SAT.h"
#include "abstract_persistence_dt.h"
#include <set>
#include <stack>
#include <utility>
#include <stdexcept>

// a wrapper for set that supports rollbacks
// use the issue_ticket() method to get an identifier, and then you can call rollback with that
// ticket, and rollback to that very point. you can also use the undo() method to undo the last change
// be careful when changing elements via reference, as such changes won't affect the rollback functionality
template<class T>
class PersistentSet : public AbstractPersistentDT<std::pair<bool, T>>{
    private:
    std::set<T> st;

    public:
    PersistentSet() {}

    template <typename... Args>// cpp dark python like magic
    auto insert(Args&&... args) {
        // still black magic, forwarding the arguments
        auto res = st.insert(std::forward<Args>(args)...);
        if (res.second) {// if was actually added
            // true for inserting, res.first is an iterator to the element added
            this->changes.push(std::pair<bool, T>(true, *res.first));
        }
        return res;// forwarding the return value
    }

    size_t erase(const T& value) { // erase by value
        size_t res = st.erase(value);
        if (res > 0) {// if was actually erased
            // false for erasing
            this->changes.push(std::pair<bool, T>(false, value));
        }
        return res;// forwarding the return value
    }

    auto erase(typename std::set<T>::iterator it) { // erase by iterator
        T value = *it; // a copy because we will erase it
        auto nextIt = st.erase(it);
        // false for erasing
        this->changes.push(std::pair<bool, T>(false, value));
        return nextIt;
    }

    // undoes the last change made, and updates changes accordingly
    void undo() override {
        if (this->changes.empty()) {
            throw std::runtime_error("no changes to undo!");
        }
        auto [is_insert, value] = this->changes.top();
        this->changes.pop();
        if (is_insert) {
            st.erase(value);// opposite of inserting is erasing
        }
        else {
            st.insert(value);// opposite of erasing is inserting
        }
    }

    size_t size() { return st.size(); }

    bool empty() { return st.empty(); }

    auto begin() { return st.begin(); }

    auto end() { return st.end(); }

    auto find(T key) { return st.find(key); }

    auto count(T key) { return st.count(key); }
    
    auto contains(T key) { return st.contains(key); }

    auto lower_bound(T key) { return st.lower_bound(key); }
    
    auto upper_bound(T key) { return st.upper_bound(key); }

    auto rbegin() { return st.rbegin(); }
};

#endif