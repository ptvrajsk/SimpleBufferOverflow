//
// Created by ubuntu on 6/15/20.
//

#include <cstring>

char* duplicateString(const char* input) {
    char* copiedCharArray = new char[50]; // Limited Size, never checked if Input Complies
    strcpy(copiedCharArray, input);
    return copiedCharArray;
}