/*
this is the cpp-side endpoint of the cpp-python communication
whenever you want to add a new solver, change name_to_solver_map
and compile with -Ofast
the executable should be named communication.exe
*/

#include<bits/stdc++.h>
#include"SAT.h"
#include "constants.h"
#include "improved_backtracking.cpp"
#include "backtracking_2sat_2furious.cpp"
using namespace std;


// a map from solver names to functions creating them
// add an entry to this map every time you add a new solver
map<string, function<AbstractSATSolver*(int)>> name_to_solver_map = {
    {"ImprovedBacktrackingSolver", [](int n){return new ImprovedBacktrackingSolver(n);}},
    {"BacktrackingSolver_V2", [](int n){return new BacktrackingSolver_V2(n);}}
};

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

    returns a solver of type solver_name
*/

AbstractSATSolver *readinput(ifstream &input_file, string solver_name){
    int num_variables, num_clauses;
    input_file >> num_variables >> num_clauses;
    if (name_to_solver_map.count(solver_name) == 0){
        cerr << "unknown solver!\n";
        exit(1);
    }
    AbstractSATSolver *solver = name_to_solver_map[solver_name](num_variables);
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

// usage: ./path input_file output_file solver_name
// reads a SAT in a format as specified by readinput
// outputs the solution array, or UNSAT if there is no solution
int main(int argc, char *argv[]){
    ios_base::sync_with_stdio(false);
    if (argc < 4){
        cerr << "invalid command arguments\n";
        return 1;
    }
    ifstream input_file(argv[1]);
    ofstream output_file(argv[2]);
    if (!input_file || !output_file){
        cerr << "invalid input/output paths\n";
        return 1;
    }
    AbstractSATSolver *solver = readinput(input_file, argv[3]);
    vector<int> answer = solver->solve();
    if (answer.size() != 0){ // there is a solution
        for (int x : answer){
            output_file << x << " ";
        }
    } else {
        output_file << "UNSAT";
    }
    
}