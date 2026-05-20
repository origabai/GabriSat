#ifndef SAT_THREADED_BACKTRACKER_H
#define SAT_THREADED_BACKTRACKER_H

#include "SAT.h"
#include "SAT_abstract_handling_DS.h"
#include "constants.h"
#include <unistd.h>
#include <signal.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <mutex>
#include <atomic>
using std::set;

// the total number of processes currently running. shared memory between all processes
// theres a race condition with checking/incrementing this value - it's not very accurate
// in practice this means the actual number of processes will be ~2-3x of num_processes
std::atomic<int> *num_processes;
// whether a solution was found, shared memory between all processes
std::atomic<bool> *solution_found;
// memory where a solution is stored when found. shared memory between all processes
int *solution_space;
// solution space write lock, shared memory between all processes
std::mutex *solution_space_mutex;
// the pid of the recursion root process
// this is not the root process, but his son
int recursion_root_pid = -1;


void quit_handler(int){
    if (recursion_root_pid > 0) kill(-getpgid(recursion_root_pid), SIGKILL);
    exit(0);
}

// abstract multiprocess backtracking solver using the handler DS
class AbstractThreadedSolver : public AbstractSATSolver{
    SATHandlingDS *handler;

    public:

    AbstractThreadedSolver(int num_variables, SATHandlingDS *ds) : AbstractSATSolver(num_variables), handler(ds) {
        num_processes = (std::atomic<int>*)mmap(NULL, sizeof(std::atomic<int>), PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_SHARED, -1, 0);
        *num_processes = 1;
        solution_found = (std::atomic<bool>*)mmap(NULL, sizeof(std::atomic<bool>), PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_SHARED, -1, 0);
        *solution_found = false;
        solution_space = (int*)mmap(NULL, sizeof(int) * num_variables, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_SHARED, -1, 0);
        solution_space_mutex = (std::mutex*) mmap(NULL, sizeof(std::mutex), PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_SHARED, -1, 0);
        signal(SIGINT, quit_handler);
    }
    
    
    std::vector<int> solve() override {
        handler->initialize(num_variables, clauses);
        recursion_root_pid = fork();
        if (recursion_root_pid == 0){
            // child
            setpgid(0,0);
            rec_solve();
            while (wait(0) > 0);
            exit(0);
        } else {
            // root process
            wait(0);
            if (!*solution_found){
                return {};
            }
            vector<int> ans(num_variables);
            for (int i=0;i<num_variables;i++){
                ans[i] = solution_space[i];
            }
            return ans;
        }
    }

    void rec_solve() {
        auto [v1, v2] = handler->fork_variable(*num_processes);
        int truthval = SAT_TRUE;
        if (rand()%2==0) truthval = SAT_FALSE;
        if (v1 != NO_NEXT_VAR){
            // fork the assignments of variables
            if (fork() == 0){
                // child
                (*num_processes)++;
                assign_variable(v1, truthval);
                (*num_processes)--;
                while (wait(0) > 0);
                exit(0);
            } else {
                // parent
                assign_variable(v2, truthval);
            }
        } else {
            // normal assignment
            auto [curr_var, truthval] = handler->next_var();
            assign_variable(curr_var, truthval);   
        }
    }
    
    // assigns a variable both true and false
    void assign_variable(int curr_var, int truthval){
        // base case
        if (curr_var == NO_NEXT_VAR){
            if (handler->valid()){
                *solution_found = true;
                vector<int> ans = handler->current_assignment();
                solution_space_mutex->lock();
                for (int i=0;i<num_variables;i++){
                    solution_space[i] = ans[i];
                }
                // a solution was found, murder everyone
                kill(0, SIGKILL);
                exit(0);
            } else {
                return;
            }
        }
        regular_assignment(curr_var, truthval);
    }

    // regular single process assignment
    void regular_assignment(int curr_var, int truthval){
        // assigns suggested value
        handle_assignment(curr_var, truthval);

        // assign opposite
        if (truthval == SAT_TRUE){
            truthval = SAT_FALSE;
        } else {
            truthval = SAT_TRUE;
        }

        handle_assignment(curr_var, truthval);

        return;
    }

    // returns whether a solution was found
    void handle_assignment(int curr_var, int truthval){
        handler->upd_assignment(curr_var, truthval);
        if (handler->valid()){
            rec_solve();
        }
        handler->rollback_assignment();
        return;
    }
};

#endif