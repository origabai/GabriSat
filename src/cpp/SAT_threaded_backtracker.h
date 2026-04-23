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

// the total number of processes currently running. shared memory between all processes
std::atomic<int> *num_processes;
// memory where a solution is stored when found. shared memory between all processes
int *solution_space;
// solution space write lock, shared memory between all processes
std::mutex *solution_space_mutex;

// housekeeping - all of the children pids of the current process
vector<int> children_pids;

// this is bound to the signal SIGUSR1
// it results in killing all of the processes in the subtree, and moving the signal upwards
void kill_upward_handler(int){
    for (int pid : children_pids){
        kill(pid, SIGUSR2);
    }
    kill(getppid(), SIGUSR1);
    exit(0);
}

// this is bound to the signal SIGUSR2
// it results in killing all of the processes in the subtree
void kill_subtree_handler(int){
    for (int pid : children_pids){
        kill(pid, SIGUSR2);
    }
    exit(0);
}

// abstract multiprocess backtracking solver using the handler DS
class AbstractThreadedSolver : public AbstractSATSolver{
    SATHandlingDS *handler;

    public:

    AbstractThreadedSolver(int num_variables, SATHandlingDS *ds) : AbstractSATSolver(num_variables), handler(ds) {
        num_processes = (std::atomic<int>*)mmap(NULL, sizeof(std::atomic<int>), PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_SHARED, -1, 0);
        *num_processes = 0;
        solution_space = (int*)mmap(NULL, sizeof(int) * num_variables, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_SHARED, -1, 0);
        solution_space_mutex = (std::mutex*) mmap(NULL, sizeof(std::mutex), PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_SHARED, -1, 0);
        // make root process ignore the signals
        signal(SIGUSR1, SIG_IGN);
        signal(SIGUSR2, SIG_IGN);
    }
    
    
    std::vector<int> solve() override {
        handler->initialize(num_variables, clauses);
        if (fork() == 0){
            // child
            signal(SIGUSR1, kill_upward_handler);
            signal(SIGUSR2, kill_subtree_handler);
            if (!rec_solve()){
                solution_space[0] = VARIABLE_UNSET;
            }
            exit(0);
        } else {
            // root process
            wait(0);
            if (solution_space[0] == VARIABLE_UNSET){
                return {};
            }
            vector<int> ans(num_variables);
            for (int i=0;i<num_variables;i++){
                ans[i] = solution_space[i];
            }
            return ans;
        }
    }
    
    // returns whether a solution was found
    bool rec_solve() {
        auto [curr_var, truthval] = handler->next_var();
        // base case
        if (curr_var == NO_NEXT_VAR){
            if (handler->valid()){
                vector<int> ans = handler->current_assignment();
                solution_space_mutex->lock();
                for (int i=0;i<num_variables;i++){
                    solution_space[i] = ans[i];
                }
                // a solution was found, murder everyone
                kill_upward_handler(0);
            }
            else return false;
        }
        if (handler->do_fork(*num_processes)){
            return fork_assignment(curr_var);
        } else {
            return regular_assignment(curr_var, truthval);
        }
    }

    bool fork_assignment(int curr_var){
        int cpid = fork();
        if (cpid == 0){
            // child
            children_pids.clear();
            *num_processes++;
            handle_assignment(curr_var, SAT_FALSE);
            *num_processes--;
            exit(0);
        } else {
            // parent
            children_pids.push_back(cpid);
            handle_assignment(curr_var, SAT_TRUE);
            // wait for all children to exit
            while (wait(0) > 0);
            return false;
        }
    }

    // regular single process assignment
    bool regular_assignment(int curr_var, int truthval){
        // assigns suggested value
        handle_assignment(curr_var, truthval);

        // assign opposite
        if (truthval == SAT_TRUE){
            truthval = SAT_FALSE;
        } else {
            truthval = SAT_TRUE;
        }

        handle_assignment(curr_var, truthval);

        return false;
    }

    // returns whether a solution was found
    bool handle_assignment(int curr_var, int truthval){
        handler->upd_assignment(curr_var, truthval);
        if (handler->valid()){
            bool found_sol = rec_solve();
            return found_sol;
        }
        handler->rollback_assignment();
        return false;
    }
};

#endif