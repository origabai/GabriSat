#include "improved_backtracking.cpp"
#include<bits/stdc++.h>
using namespace std;

int main(){
    int n = 4;
    ImproverBacktrackingSolver solver(11);
    solver.addClause({2}, {5});
    solver.addClause({1}, {6});
    solver.addClause({}, {10,6});
    solver.addClause({}, {4,5});
    solver.addClause({2}, {6});
    solver.addClause({}, {5,6});
    solver.addClause({8,9}, {});
    solver.addClause({}, {3,5});
    solver.addClause({8}, {7});
    solver.addClause({}, {7,10});
    vector<int> ans = solver.solve();
    for (int x : ans){
        cout << x << " ";
    }
}