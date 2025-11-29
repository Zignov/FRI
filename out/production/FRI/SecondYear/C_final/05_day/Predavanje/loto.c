//
// Created by Žiga Novak on 26. 9. 25.
//

#include <stdlib.h>
#define N 7
#define MAX 38
#include <stdio.h>
#include <time.h>



void uredi(int tab[], int n) {
    for (int i = 0; i < n-1; ++i) {
        for (int j = 0; j< n-i-1; ++j) {
            if (tab[j] > tab[j+1]) {
                int temp = tab[j];
                tab[j] = tab[j+1];
                tab[j+1] = temp;
            }
        }
    }
}

int main(int argc, char *argv[]) {
    int loto[N];

    int stevila[MAX];
    for (int i = 0; i<MAX; i++) {
        stevila[i] = i+1;
    }

    srand(time(NULL));

    int razpon = MAX;
    for (int i = 0; i< N; ++i) {
        int x = rand() % razpon;
        loto [i] = stevila[x];
        stevila[x] = stevila[razpon - 1];
        razpon--;
    }

    uredi(loto, N);

    for (int i = 0; i < N; ++i) {
        printf("%d ", loto[i]);
    }
}
