# this file should contain the compilation command used to create communication.exe

g++ -static -Ofast communication.cpp -o communication.exe

# new windows compilation for increased stack size:
# g++ -static -Ofast src/cpp/communication.cpp -o src/cpp/communication.exe "-Wl,--stack,67108864"