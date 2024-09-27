#!/bin/bash
mkdir -p build &&
gcc -o build/libhomie.o -c -mincoming-stack-boundary=3 -nostdlib -fno-stack-protector libhomie.c &&
python3 src/main.py main.hom > build/main.asm &&
nasm -f elf64 -o build/main.o build/main.asm &&
ld build/main.o build/libhomie.o -o build/program.out &&
./build/program.out
