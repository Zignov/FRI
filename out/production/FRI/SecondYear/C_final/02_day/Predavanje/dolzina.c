//
// Created by Žiga Novak on 23. 9. 25.
//

#include <stdio.h>
#include <string.h>

int dolzina(char niz[]) {
    int d = 0, i = 0;

    while (niz[i] != '\0') d++, i++;
    return d;
}

int main() {
    char a[] = "Hello World";
    printf("dolzina od %s je %d\n", a, dolzina(a));
}