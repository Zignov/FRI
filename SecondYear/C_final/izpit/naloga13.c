//
// Created by Žiga Novak on 13. 10. 25.


#include <stdio.h>
#include <stdlib.h>

typedef struct elt {
    int x;
    struct elt *next;
    struct elt *prev;
}elt;


elt* push(elt* skladi, int x) {
    elt *tmp = malloc(sizeof(elt));

    tmp->x = x;
    tmp->prev = NULL;
    tmp->next = skladi;

    if (skladi != NULL) {
        skladi->prev = tmp;
    }
    return tmp;
}

elt* pop(elt* skladi) {
    elt *star = skladi;
    elt *nov = skladi->next;
    skladi = skladi->next;
    free (star);
    if (skladi -> next != NULL) {
        skladi->next->prev = NULL;
    }
    return nov;
}

int vrh(elt* skladi) {
    elt *tmp = skladi;
    return (tmp -> x);
    free(tmp);
}

void izpisi(elt* skladi, int nacin) {
    if (nacin == 0) {
        while (skladi != NULL) {
            printf("%d ", skladi->x);
            skladi = skladi->next;
        }
    }
    if (nacin == 1) {
        while (skladi->next != NULL) {
            skladi = skladi->next;
        }

        while (skladi != NULL) {
            printf("%d ", skladi -> x);
            skladi = skladi->prev;
        }
    }
    printf("\n");
}


int main(int argc, char **args) {
    elt * sklad = NULL;

    sklad=push(sklad, 5);
    sklad=push(sklad, 3);
    sklad=push(sklad, 1);

    int x = vrh(sklad);
    printf("Na vrhu sklada je število %d\n", x);

    sklad=pop(sklad);
    sklad=push(sklad, 4);
    sklad=push(sklad, 3);
    sklad=pop(sklad);

    printf("Vsebina sklada (od zgoraj navzdol): ");
    izpisi(sklad, 0);

    printf("Vsebina sklada (od spodaj navzgor): ");
    izpisi(sklad, 1);
}
