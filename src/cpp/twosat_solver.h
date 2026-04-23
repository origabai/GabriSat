#ifndef TWOSAT_SOLVER
#define TWOSAT_SOLVER
#include "constants.h"
#include "SAT.h"
#include<vector>
#include<utility>
#include<stack>
#include<queue>
using std::pair, std::vector, std::stack, std::queue;


// solver for a 2SAT problem
class TwoSATSolver : AbstractSATSolver {
    // implication graph.
    // positive literals are [0,n-1], negative literals are [n, 2n-1]
    vector<vector<int>> graph_out, graph_in;
    // visited nodes
    vector<bool> visited;
    // graph nodes by dfs-out order
    stack<int> ord;
    // connected component of node i is component[i]
    vector<int> component;

    
    // opposite of a variable index
    int opp(int x){
        if (x >= num_variables){
            return x - num_variables;
        } else {
            return x + num_variables;
        }
    }

    // calculate dfs-out order of the out-graph
    void dfs1(int v){
        if (visited[v]) return;
        visited[v] = true;
        for (int u : graph_out[v]){
            if (!visited[u]) dfs1(u);
        }
        ord.push(v);
    }
    
    // second dfs to calculate SCC
    void dfs2(int timer, int v){
        if (visited[v]) return;
        visited[v] = true;
        component[v] = timer;
        for (int u : graph_in[v]){
            if (!visited[u]) dfs2(timer,u);
        }
    }

    // topologically sorts the graph
    vector<int> topsort(vector<int> out[], int n){
        vector<int> deg(n,0);
        for (int i=0; i<n; i++){
            for (int u : out[i]) deg[u]++;
        }
        queue<int> q;
        for (int i=0; i<n; i++){
            if (deg[i] == 0)q.push(i);
        }
        vector<int> ans;
        while (q.size()){
            int v = q.front();
            ans.push_back(v);
            q.pop();
            for (int u : out[v]){
                deg[u]--;
                if (deg[u] == 0){
                    q.push(u);
                }
            }
        }
        return ans;
    }

    public:
    // initializes the solver
    TwoSATSolver(int num_variables) : AbstractSATSolver(num_variables), graph_out(2 * num_variables), graph_in(2 * num_variables),
     visited(2 * num_variables, false), component(2 * num_variables) {}

    void addClause(std::set<int> pos, std::set<int> neg) override{
        int u,v;
        if (pos.size() + neg.size() == 2){
            if (pos.size() == 2){
                u = *pos.begin();
                v = *pos.rbegin();
            } else if (pos.size() == 1){
                u = *pos.begin();
                v = num_variables+ *neg.begin();
            } else {
                u = num_variables + *neg.begin();
                v = num_variables + *neg.rbegin();
            }
        } else if (pos.size() + neg.size() == 1){
            if (pos.size()){
                u = v = *pos.begin();
            } else {
                u = v = num_variables + *neg.begin();
            }
        } else {
            return;
        }
        graph_out[opp(u)].push_back(v);
        graph_in[v].push_back(opp(u));
        graph_out[opp(v)].push_back(u);
        graph_in[u].push_back(opp(v));
    }

    std::vector<int> solve() override{
        // calculate the dfs out order, and store it in the stack "ord"
        for (int i=0; i<2*num_variables; i++){
            dfs1(i);
        }
        visited.assign(2 * num_variables, 0);
        int timer = 0;
        
        // go over nodes by dfs-out order to find components
        while (ord.size()){
            int v = ord.top();
            ord.pop();
            if (visited[v]) continue;
            dfs2(timer++,v);
        }
        for (int v=0; v<num_variables; v++){
            if (component[v] == component[v+num_variables]){
                return {};
            }
        }

        // find scc
        vector<int> gscc[timer];
        for (int v=0; v<2*num_variables; v++){
            for (int u : graph_out[v]){
                if (component[v]!=component[u]) gscc[component[v]].push_back(component[u]);
            }
        }
        // topological sort
        vector<int> srt = topsort(gscc, timer);
        vector<int> inv(timer);
        for (int i=0; i<timer; i++){
            inv[srt[i]] = i;
        }
        vector<int> ans(num_variables);
        for (int i=0; i<num_variables; i++){
            if (inv[component[i]] < inv[component[i+num_variables]]){
                ans[i] = SAT_FALSE;
            } else {
                ans[i] = SAT_TRUE;
            }
        }
        return ans;
    }
};
#endif