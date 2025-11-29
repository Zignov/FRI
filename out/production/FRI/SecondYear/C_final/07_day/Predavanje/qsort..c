//
// Created by Žiga Novak on 30. 9. 25.
//


#include <stdlib.h>
#include <stdio.h>

int primerjaj(const void *a, const void *b) {
    int o1 = *((int *)a);
    int o2 = *((int *)b);

    return o1 - o2;
}


int main(int argc, char *argv[]) {
    int tab[] = {3,5,3,2,4,5,6,7,3,1,3,42,6,7,4,8,9,4,3};

    int n = sizeof(tab)/sizeof(tab[0]);

    qsort(tab, n, sizeof(int), &primerjaj);
    for (int i = 0; i<n; i++) {
        printf("%d ", tab[i]);
    }
}
