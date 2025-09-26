//
// Created by Žiga Novak on 26. 9. 25.
//

#define N 100


#include <stdio.h>
#include <stdlib.h>
#include <time.h>


int main(int argc, char *argv[]) {

    if (argc != 3) {
        exit(1);
    }

    int m = atoi(argv[1]);
    int vrh = atoi(argv[2]);
    int stevila[m];
    int stevec[10];
    int maximum = 0;
    srand(time(NULL));

    for (int i = 0; i<10; i++) {
        stevec[i] = 0;
    }

    for (int i = 0; i < m; i++) {
        stevila[i] = rand() % N;

        int lokacija = stevila[i] / 10;

        if (++stevec[lokacija] > maximum) {
            maximum = stevec[lokacija];
        }
        //printf("st: %d\n", stevila[i]);
    }

    for (int i = 0; i<10; i++) {

        stevec[i] = ((stevec[i] * vrh) / maximum);
        //printf("stevila: %d, vrh: %d, max: %d\n", stevila[i], vrh, maximum);
    }

    for (int i = 0; i<10; i++) {
        printf("%d - %d: ", 10 * i+1, 10 *i+10);

        for (int j = 0; j<stevec[i]; j++) {
            printf("%c", 'o');
        }

        printf(" (%d) \n", stevec[i]);
    }

}
