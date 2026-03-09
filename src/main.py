from SAT import SAT
def main():
    s = SAT(3)
    
    s.addClause([0,1],[2])
    s.addClause([0,2],[])
    print(s.solve())
    pass

if __name__ == "__main__":
    main()