//
// Created by ubuntu on 6/15/20.
//

#include <cstdlib>
#include "../../app/src/main/cpp/libstrcpy.cpp"

extern "C" int LLVMFuzzerTestOneInput(const char* Data, size_t size) {
    if (size >= 1) {
        if (Data[size-1] == '\0') {
            char* a = duplicateString(Data);
            delete[] a;    
        }
    }
    return 0;
}