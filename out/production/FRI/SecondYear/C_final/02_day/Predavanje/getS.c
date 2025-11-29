//
// Created by Žiga Novak on 23. 9. 25.
//
#define N 100
#include <stdio.h>

int main() {
    char vrstica[N];

    fgets(vrstica, N ,stdin);
    printf("%s\n", vrstica);
}