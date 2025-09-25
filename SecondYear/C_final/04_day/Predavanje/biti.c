//
// Created by Žiga Novak on 25. 9. 25.
//

#include <stdio.h>


int stBitov1(int x) {
    int rez = 0;
    while (x!=0) {
        if (x%2 == 1) {
            rez++;
        }
        x /= 2;
    }
    return rez;
}

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


int stBitov3(int x) {
    int rez = 0;
    while (x!=0) {
        rez++;
        x = x & (x-1);
    }
    return rez;
}

int main() {
    int x = 42;

    printf("Stevilo prizganih bitov v %d je %d", x, stBitov3(x));
}