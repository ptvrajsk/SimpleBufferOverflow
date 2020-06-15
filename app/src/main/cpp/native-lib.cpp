#include <jni.h>
#include <string>

extern "C" JNIEXPORT jstring JNICALL
Java_com_example_simplebufferoverflow_MainActivity_stringFromJNI(
        JNIEnv* env,
        jobject jobj,
        jstring userInput) {

    char* copiedCharArray = new char[50]; // Limited Size, never checked if Input Complies

    // If Input > 50 len, buffer overflow is executed.
    const char* charArr = env->GetStringUTFChars(userInput, JNI_FALSE);
    strcpy(copiedCharArray, charArr);

    env->ReleaseStringUTFChars(userInput, charArr);

    return env->NewStringUTF(copiedCharArray);
}
