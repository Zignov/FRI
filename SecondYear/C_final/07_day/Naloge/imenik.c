//
// Created by Žiga Novak on 30. 9. 25.
//


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *ime;
    char *priimek;
    char *telefon;
} oseba;


int sortiranje(const void *a, const void *b) {
    oseba *o1 = a;
    oseba *o2 = b;

    int c = strcmp(o1->priimek, o2->priimek);
    return c;
}

int main() {
    int steviloVrstic;
    FILE *f = fopen("osebe.txt", "r");
    char vrstica[100];
    char delim[] = ":";
    char *ime;
    char *priimek;
    char *telefon;
    int rezervacija;
    int skupaj = 0;


    fscanf(f, "%d", &steviloVrstic);
    oseba *osebe = malloc(steviloVrstic* sizeof(oseba));
    skupaj += (steviloVrstic * sizeof(oseba));


    for (int i = 0; i < steviloVrstic; i++) {
        //if (i==0) continue;

        fscanf(f, "%s", vrstica);

        ime = strtok(vrstica, delim);
        priimek = strtok(NULL, delim);
        telefon = strtok(NULL, delim);

        rezervacija = strlen(ime) + 1;
        skupaj += rezervacija;
        osebe[i].ime = malloc(rezervacija);
        strcpy(osebe[i].ime, ime);
        //printf("rezervacija :%d\n", skupaj);



        rezervacija = strlen(priimek)+1;
        skupaj += rezervacija;
        osebe[i].priimek = malloc(rezervacija);
        strcpy(osebe[i].priimek, priimek);


        rezervacija = strlen(telefon)+1;
        skupaj += rezervacija;
        osebe[i].telefon = malloc(rezervacija);
        strcpy(osebe[i].telefon, telefon);



        //printf("%s - velikost:%d\n", razdeljeno,rezervacija);
    }

    qsort(osebe, steviloVrstic, sizeof(oseba), &sortiranje);


    for (int i = 0; i < steviloVrstic; i++) {
        printf("%s %s - %s\n", osebe[i].ime, osebe[i].priimek, osebe[i].telefon);

    }

    printf("skupaj: %d\n", skupaj);
    //printf("Size: %d", sizeof(char));

    for (int i = 0; i< steviloVrstic; i++) {
        free(osebe[i].ime);
        free(osebe[i].priimek);
        free(osebe[i].telefon);
    }
    free(osebe);
}