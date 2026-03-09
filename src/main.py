from SAT import SAT
def main():
    s = SAT(3)
    s.addClause([1,2,3],[4])
    s.addClause([2,3],[1])
    s.addClause([])
    s.solve()

if __name__ == "__main__":
    main()