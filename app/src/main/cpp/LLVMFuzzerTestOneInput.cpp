//
// Created by ubuntu on 6/14/20.
//
#include <cstddef>
#include <cstdint>
#include "native-lib.cpp"


extern "C" jstring LLVMFuzzerTestOneInput(JNIEnv* env,
                                      jobject jobj,
                                      jstring userInput) {
    // ...
    // Use the data to call the library you are fuzzing.
    // ...
    return Java_com_example_simplebufferoverflow_MainActivity_stringFromJNI(env, jobj, userInput);
}




