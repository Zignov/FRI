//
// Created by Žiga Novak on 1. 10. 25.
//


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void zlij(int *t, int z, int k) {
    int s = (z+k)/2;
    int i = z;
    int j = s+1;
    int n = 0;

    int *nova = malloc(sizeof(int) * (k-z+1));
    while (i<=s && j<=k) {
        if (t[i] < t[j]) {
            nova[n] = t[i];
            i++;
        }
        else {
            nova[n] = t[j];
            j++;
        }
        n++;
    }


    while (i<=s) {
        nova[n++] = t[i++];
    }

    /*for (i = 0; i<n; i++) {
        t[z+i] = nova[i];
    }*/

    memcpy(t+z, nova, sizeof(int) * n);
    free(nova);
}

void mergesort2(int *t, int z, int k) {
    if (z<k) {
        int s = (z+k)/2;
        mergesort2(t, z, s);
        mergesort2(t, s+1, k);
        zlij(t,z,k);
    }
}

int main(int argc, char *argv[]) {
    int tab[] = {4,5,2,1,4,6,8,5,3,6,7,3};
    int n = sizeof(tab)/sizeof(tab[0]);

    mergesort2(tab, 0, n-1);

    for (int i=0; i<n; ++i) {
        printf("%d ", tab[i]);
    }
}
