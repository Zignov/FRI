//
// Created by Žiga Novak on 25. 9. 25.
//
#include <stdlib.h>
#include <stdio.h>

int stBitov2(int x) {
    int rez = 0;
    while (x>0) {
        if ((x & 1) != 0) {
            rez++;
        }
        x = x>>1;
    }
    return rez;
}

void printBits(int x) {
    for (int i = 7; i>=0; i--) {
        printf("%d", (x & (1<<i)) != 0);
    }
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        exit(1);
    }

    int x = 0;
    int biti = atoi(argv[1]);
    int sestevek = 0;
    int stevec = 0;

    while (x<256) {
        if (stBitov2(x) == biti) {
            printBits(x);
            printf(" = %d\n", x);
            sestevek+=x;
            stevec++;
        }
        x++;
    }

    printf("i=%d, n=%d, sestevek=%d", biti, stevec, sestevek);
}

