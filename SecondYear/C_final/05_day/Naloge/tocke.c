//
// Created by Žiga Novak on 26. 9. 25.
//

#include <math.h>
#include <stdio.h>
#include <string.h>
#define N 100

struct tocka {
    char ime[5];
    float x;
    float y;
};

void izpis(struct tocka tab[], int dolzina) {
    for (int i = 0; i<dolzina; i++) {
        printf("%s %.02f %.02f\n", tab[i].ime, tab[i].x, tab[i].y);
    }
}

void uredi(struct tocka tab[], int dolzina) {
    for (int i = 0; i<dolzina-1; ++i) {
        for (int j = 0; j<dolzina-i-1; ++j) {
            if (strcmp(tab[j].ime, tab[j+1].ime) > 0) {
                struct tocka temp = tab[j];
                tab[j] = tab[j+1];
                tab[j+1] = temp;
            }
        }
    }
}


void uredi2(struct tocka tab[], int dolzina) {
    for (int i = 0; i<dolzina-1; ++i) {
        for (int j = 0; j<dolzina-i-1; ++j) {
            int a = sqrt((tab[j].x * tab[j].x) + (tab[j].y * tab[j].y));
            int b = sqrt((tab[j+1].x * tab[j+1].x) + (tab[j+1].y * tab[j+1].y));

            if (a>b) {
                struct tocka temp = tab[j];
                tab[j] = tab[j+1];
                tab[j+1] = temp;
            }
        }
    }}

int main(int argc, char *argv[]) {
    int i = 0;
    struct tocka tab[N];

    FILE *vhod = fopen(argv[1], "r");
    while (!feof(vhod)) {

        fscanf(vhod, "%s %f %f", tab[i].ime, &tab[i].x, &tab[i].y);
        i++;
    }

    izpis(tab, --i);
    printf("//////////////////////\n");
    uredi(tab, i);
    izpis(tab, i);
    printf("////////////////////\n");
    uredi2(tab, i);
    izpis(tab, i);
}

