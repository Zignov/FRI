//
// Created by Žiga Novak on 25. 9. 25.
//

#include <stdio.h>
#include <stdlib.h>
#define N 100

int main() {
    FILE *f;

    f = fopen("file.txt", "r");
    if (f == NULL) {
        exit(1);
    }

    int i = 1;
    char vrstica[N];
    int nova = 1;


    while (!feof(f)) {
        fgets(vrstica, N, f);

        printf("%d. %s", i, vrstica);
    }


    fclose(f);
}