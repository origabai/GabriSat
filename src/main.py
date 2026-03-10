from hamiltonian_cycle import Hamiltonian_Cycle
def main():
    h = Hamiltonian_Cycle(0,[])
    h.generate_from_input()
    print(h.solve())

if __name__ == "__main__":
    main()