//
// Created by Žiga Novak on 22. 9. 25.
//

#include <stdlib.h>
#include <stdio.h>
#include <time.h>

int main() {
    srand(time(NULL));

    int n = 1000;
    int vKrogu = 0;
    for (int i = 0; i < n; i++) {
        double x = rand() / (double) RAND_MAX;
        double y = rand() / (double) RAND_MAX;

        if (x*x + y*y <= 1) vKrogu++;
    }

    printf("pi = %.6f\n", (double)4*vKrogu/n);
}