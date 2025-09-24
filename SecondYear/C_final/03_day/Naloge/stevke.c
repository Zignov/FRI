//
// Created by Žiga Novak on 24. 9. 25.
//

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#define N 100

void prestej(char niz[], int pojavitve[]) {
    for (int i = 0; niz[i] != '\0'; i++) {
        int stevka = (niz[i]) - '0';

        //printf("%d\n", stevka);

        pojavitve[stevka]++;

    }
}

int main() {

    char niz[N];
    char trenutna[N];

    while (true) {
        fgets(trenutna, N, stdin);
        if (strlen(trenutna) == 1) {
            break;
        }
        else {
            strcat(niz, trenutna);
        }

    }
    int pojavitve[10];

    for (int i = 0; i<10; i++) {
        pojavitve[i] = 0;
    }

    prestej(niz, pojavitve);

    for (int i = 0; i<10; i++) {
        printf("%i = %d, ",i, pojavitve[i]);
    }
}
