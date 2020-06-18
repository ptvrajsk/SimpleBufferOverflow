# SimpleBufferOverflow (Native C++)

## Vulnerable Code

The vulnerable area of code can be found in `../cpp/libstrcpy.cpp` which has an array of a **fixed length** that is used in `strcpy` that copies an **unchecked length** string into that array.

The app is already compiled with ASAN at the moment so writing an input > than expected size will cause a crash and a logcat dump of the ASAN report.

## UI-Fuzzer

The UI based fuzzer that uses `gdb` is located in te `fuzz/ui` directory. For usage information use `python3 uiFuzz.py --help`. The tool has not been crafted to activate the emulator on its own so you need to be running the emulator before using it.

## libfuzzer

The `libfuzzer` test code is in `fuzz/libfuzzer`. To compile the test code with `libfuzzer` and `ASAN` use 
- `clang -g -O1 -fsanitize=fuzzer,address fuzz/libfuzzer/my_target.cpp -o targetFuzzer.o`

OR

- `clang++ fsanitize=address,fuzzer fuzz/libfuzzer/my_target.cpp -o targetFuzzer.o`

After compilation use

- `./targetFuzzer.o` to run the fuzzer directly.
- `./targetFuzzer.o -help=1` to print the help page for possible options.

(More information can be found in the libfuzzer/llvm [site](https://llvm.org/docs/LibFuzzer.html).)

## afl

Test code for utilising afl is in `fuzz/afl`. You need to have cloned afl into your machine and use `afl-g++` to compile the source code (it works similar to g++). Post comiplation, you can run the fuzzer with `afl-fuzz <compileoutput> -i <corpusdir> -o <outputdir>`.

(More information can be found in the google/afl [repo](https://github.com/google/AFL).)