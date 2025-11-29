//
// Created by Žiga Novak on 29. 9. 25.
//


#include <stdlib.h>
#include <stdio.h>

typedef struct sklad {
    int velikost;
    int kazalec;
    int *tabela;
};

void init(int velikost, struct sklad *s) {

    s -> velikost = velikost;
    s -> kazalec = -1;
    s -> tabela = malloc(sizeof(int) * velikost);
}

void push(int x, struct sklad *s) {
    if (++s->kazalec <= s->velikost ) {
        s->tabela[s->kazalec] = x;
    }
}

void pop(struct sklad *s) {
    printf("Izbrisano: %d\n", s->tabela[s->kazalec--]);
}

int isEmpty(struct sklad *s) {
    return s->kazalec == -1;
}