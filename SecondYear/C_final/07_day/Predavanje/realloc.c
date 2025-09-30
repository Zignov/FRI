//
// Created by Žiga Novak on 30. 9. 25.
//

#include <stdlib.h>

void razsiri(int **p, int *n) {
    int *nova = malloc(sizeof(int) * (*n+1));
    for (int i = 0; i<*n; i++) {
        nova[i] = *p[i];
    }
    free(p);
    *p = nova;

    (*n)++;
}

int main(int argc, char *argv[]) {
    int n = 10;
    int *tabela = malloc(n*sizeof(int));

    razsiri(&tabela, &n);
}
