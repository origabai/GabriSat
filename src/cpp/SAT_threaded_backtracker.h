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
std::atomic<int> *num_processes;
// whether a solution was found, shared memory between all processes
std::atomic<bool> *solution_found;
// memory where a solution is stored when found. shared memory between all processes
int *solution_space;
// solution space write lock, shared memory between all processes
std::mutex *solution_space_mutex;
// the pid of the root process
int rootpid;

void sighandler(int){
    if (getpid() != rootpid){
        exit(0);
    }
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
        rootpid = getpid();
        signal(SIGUSR1, sighandler);
    }
    
    
    std::vector<int> solve() override {
        handler->initialize(num_variables, clauses);
        if (fork() == 0){
            // child
            std::cout << getpid() << " " << __LINE__ << std::endl;
            bool fl = rec_solve();
            exit(0);
        } else {
            // root process
            std::cout << getpid() << " " << __LINE__ << " " << *solution_found << std::endl;
            wait(0);
            std::cout << getpid() << " " << __LINE__ << " " << *solution_found << std::endl;
            if (!*solution_found){
                return {};
            }
            vector<int> ans(num_variables);
            for (int i=0;i<num_variables;i++){
                ans[i] = solution_space[i];
            }
            std::cout << getpid() << " " << __LINE__ << std::endl;
            return ans;
        }
    }
    
    // returns whether a solution was found
    bool rec_solve() {
        std::cout << getpid() << " " << __LINE__ << std::endl;
        auto [curr_var, truthval] = handler->next_var();
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
                std::cout << getpid() << " " << __LINE__ << std::endl;
                kill(0, SIGUSR1);
                std::cout << getpid() << " " << __LINE__ << std::endl;
                exit(0);
            } else {
                return false;
            }
        }
        if (handler->do_fork(*num_processes)){
            return fork_assignment(curr_var);
        } else {
            return regular_assignment(curr_var, truthval);
        }
    }

    bool fork_assignment(int curr_var){
        std::cout << getpid() << " " << __LINE__ << std::endl;
        if (*solution_found){
            for (;;){
                sched_yield();
            }
        }
        int cpid = fork();
        if (cpid == 0){
            // child
            (*num_processes)++;
            handle_assignment(curr_var, SAT_FALSE);
            (*num_processes)--;
            exit(0);
        } else {
            // parent
            handle_assignment(curr_var, SAT_TRUE);
            // wait for all children to exit
            while (wait(0) > 0);
            std::cout << getpid() << " " << __LINE__ << std::endl;
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
            rec_solve();
        }
        handler->rollback_assignment();
        return false;
    }
};

#endif