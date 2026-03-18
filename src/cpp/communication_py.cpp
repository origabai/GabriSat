/*
this is the cpp-side endpoint of the cpp-python communication
in order for this to work, change DEFAULT_SOLVER in constants.h
to the solver you want, and compile this file.
put the executable in cpp_executables
*/

#include<bits/stdc++.h>
#include"SAT.h"
#include "constants.h"
#include "improved_backtracking.cpp"
using namespace std;

/*
    reads sat problem from input in the following format:
    num_variables num_clauses
    num_pos_variables_1
    pos_variables_1
    num_neg_variables_1
    neg_variables_1
    ...
    num_pos_variables_m
    pos_variables_m
    num_neg_variables_m
    neg_variables_m
*/
DEFAULT_SOLVER *readinput(ifstream &input_file){
    int num_variables, num_clauses;
    input_file >> num_variables >> num_clauses;
    DEFAULT_SOLVER *solver = new DEFAULT_SOLVER(num_variables);
    for (int i=0;i<num_clauses;i++){
        int pos_num;
        input_file >> pos_num;
        set<int> pos;
        for (int j=0;j<pos_num;j++){
            int x;
            input_file >> x;
            pos.insert(x);
        }
        int neg_num;
        input_file >> neg_num;
        set<int> neg;
        for (int j=0;j<neg_num;j++){
            int x;
            input_file >> x;
            neg.insert(x);
        }
        solver->addClause(pos, neg);
    }
    return solver;
}

// usage: ./path input_file output_file
// reads a SAT in a format as specified by readinput
// outputs the solution array
int main(int argc, char *argv[]){
    if (argc < 3){
        cerr << "invalid command arguments\n";
        return 0;
    }
    ifstream input_file(argv[1]);
    ofstream output_file(argv[2]);
    if (!input_file || !output_file){
        cerr << "invalid input/output paths\n";
        return 0;
    }
    DEFAULT_SOLVER *solver = readinput(input_file);
    vector<int> answer = solver->solve();
    for (int x : answer){
        output_file << x << " ";
    }
}