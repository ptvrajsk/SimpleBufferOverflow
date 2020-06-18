#include "./app/src/main/cpp/libstrcpy.cpp"
#include <cstdlib>
#include <iostream>
#include <fstream>

extern "C" int main() {
    std::string userInput;
    std::cin >> userInput;
    char* a = duplicateString(userInput.c_str());
    delete [] a;
    return 0;
}