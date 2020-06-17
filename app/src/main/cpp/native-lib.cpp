#include <jni.h>
#include "libstrcpy.cpp"

extern "C" JNIEXPORT jstring JNICALL
Java_com_example_simplebufferoverflow_MainActivity_stringFromJNI(
        JNIEnv* env,
        jobject jobj,
        jstring userInput) {
    // If Input > 50 len, buffer overflow is executed.
    const char* charArr = env->GetStringUTFChars(userInput, JNI_FALSE);
    const char* newlyAllocatedCharArr = duplicateString(charArr);
    env->ReleaseStringUTFChars(userInput, charArr);

    return env->NewStringUTF(newlyAllocatedCharArr);
}