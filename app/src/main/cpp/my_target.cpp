//
// Created by ubuntu on 6/15/20.
//

#include <cstdlib>
#include "libstrcpy.cpp"

extern "C" int LLVMFuzzerTestOneInput(const char* Data, size_t size) {
    if (size >= 1) {
        char* workingData = (char*)malloc(sizeof(char)*size);
        for (int i = 0; i < size-1; i ++) {
            workingData[i] = Data[i];
        }
        workingData[size-1] = '\0';
        char* a = duplicateString(workingData);
        delete[] a;
        free(workingData);
    }
    return 0;
}