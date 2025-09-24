
#include <stdio.h>

int main(int argc, char *args[]){

    printf("Stevilo podanih argmuentov: %d\n", argc);
    printf("args[0]: %s\n", args[0]);


    for (int i = 1; i<argc; i++){
        printf("argument %d: %s", i, args[i]);
    }
}