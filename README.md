# SimpleBufferOverflow (Native C++)

## Vulnerable Code

The vulnerable area of code can be found in `../cpp/libstrcpy.cpp` which has an array of a **fixed length** that is used in `strcpy` that copies an **unchecked length** string into that array.

The app is already compiled with ASAN at the moment so writing an input > than expected size will cause a crash and a logcat dump of the ASAN report.

## UI-Fuzzer

The UI based fuzzer that uses `gdb` is located in te `fuzz/ui` directory. For usage information use `python3 uiFuzz.py --help`. The tool has not been crafted to activate the emulator on its own so you need to be running the emulator before using it.

## libfuzzer

The `libfuzzer` test code is in `../cpp/my_target.cpp`. To compile the test code with `libfuzzer` and `ASAN` use 
- `clang -g -O1 -fsanitize=fuzzer,address ../cpp/my_target.cpp -o targetFuzzer.o`

OR

- `clang++ fsanitize=address,fuzzer ../cpp/my_target.cpp -o targetFuzzer.o`

After compilation use

- `./targetFuzzer.o` to run the fuzzer directly.
- `./targetFuzzer.o -help=1` to print the help page for possible options.

(More information can be found in the libfuzzer/llvm [site](https://llvm.org/docs/LibFuzzer.html).)
