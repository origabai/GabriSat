#ifndef PERSISTENT_VECTOR_H
#define PERSISTENT_VECTOR_H
#include "SAT.h"
#include "abstract_persistence_dt.h"
#include <vector>
#include <stack>
#include <utility>
#include <stdexcept>

// a wrapper for vector that supports rollbacks
// use the issue_ticket() method to get an identifier, and then you can call rollback with that
// ticket, and rollback to that very point. you can also use the undo() method to undo the last change
// be careful with iterating over it by reference, as such changes won't affect the rollback functionality
template<class T>
class PersistentVector : public AbstractPersistentDT<std::pair<int, T>>{
    private:
    std::vector<T> vec;

    class Element {
        PersistentVector<T>& parent;
        int ind;
        public:
        Element(PersistentVector<T>& parent, int ind): parent(parent), ind(ind) {}
        // intercepting changes made to elements
        Element& operator=(const T& value) {
            parent.change(ind, value); // report change
            return *this;
        }
        Element& operator+=(const T& value) {
            parent.change(ind, parent.vec[ind] + value); // report change
            return *this;
        }
        Element& operator-=(const T& value) {
            parent.change(ind, parent.vec[ind] - value); // report change
            return *this;
        }
        Element& operator*=(const T& value) {
            parent.change(ind, parent.vec[ind] * value); // report change
            return *this;
        }
        Element& operator/=(const T& value) {
            parent.change(ind, parent.vec[ind] / value); // report change
            return *this;
        }
        Element& operator&=(const T& value) {
            parent.change(ind, parent.vec[ind] & value); // report change
            return *this;
        }
        Element& operator|=(const T& value) {
            parent.change(ind, parent.vec[ind] | value); // report change
            return *this;
        }
        Element& operator%=(const T& value) {
            parent.change(ind, parent.vec[ind] % value); // report change
            return *this;
        }
        Element& operator++() { // ++e
            T new_value = parent.vec[ind];
            new_value++;
            parent.change(ind, new_value); // report change
            return *this;
        }
        Element& operator--() { // --e
            T new_value = parent.vec[ind];
            new_value--;
            parent.change(ind, new_value); // report change
            return *this;
        }
        T operator++(int) { // e++
            T old_value = parent.vec[ind];
            T new_value = parent.vec[ind];
            new_value++;
            parent.change(ind, new_value); // report change
            return old_value;
        }
        T operator--(int) { // e--
            T old_value = parent.vec[ind];
            T new_value = parent.vec[ind];
            new_value--;
            parent.change(ind, new_value); // report change
            return old_value;
        }
        // a cast to the actual type
        operator T() const {
            return parent.vec[ind];
        }
    };

    public:
    PersistentVector() {}
    PersistentVector(int size) : vec(size) {}
    PersistentVector(int size, T value) : vec(size, value) {}

    // returns an Element object that will call change() whenever it's changed
    Element operator[](int ind) {
        return Element(*this, ind);
    }
    // returns a read only object
    const T& operator[](int ind) const {
        return vec[ind];
    }

    // undoes the last change made, and updates changes accordingly
    void undo() override {
        if (this->changes.empty()) {
            throw std::runtime_error("vector is empty! nothing to undo!");
        }
        auto [ind, value] = this->changes.top();
        this->changes.pop();
        vec[ind] = value;
    }

    void change(int ind, T value) {
        this->changes.push(std::pair<int, T>(ind, vec[ind]));
        vec[ind] = value;
    }

    size_t size() { return vec.size(); }
    
    bool empty() { return vec.empty(); }

    auto begin() { return vec.begin(); }

    auto end() { return vec.end(); }
};

#endif