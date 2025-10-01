//
// Created by Žiga Novak on 1. 10. 25.
//

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX 100


typedef struct bes {
    char beseda[MAX];
    struct bes *nasl; // kazalec na naslednji element seznama
    struct bes *nasCrka;
} beseda;

typedef int fIsci(beseda *, char *);

void dodajBesedo(beseda ** glava, char *bes) {

    beseda *nov =malloc(sizeof(beseda));


    strcpy(nov->beseda, bes);
    nov->nasl = NULL;
    nov->nasCrka = NULL;

    if (*glava == NULL || strcmp((*glava)->beseda, bes) > 0) {
        nov -> nasl = *glava;
        *glava = nov;

        return;
    }


    if (strcmp((*glava)->beseda, bes) == 0) return;
    beseda *temp = *glava;

    while (temp -> nasl != NULL && strcmp(temp -> nasl -> beseda, bes) < 0){
        temp = temp -> nasl;
    }

    if (temp->nasl && strcmp(temp->nasl->beseda, bes) == 0) return;


    strcpy(nov->beseda, bes);
    nov->nasl = temp->nasl;
    temp->nasl = nov;
}






char * male (char orig[]){
    for (int i = 0; orig[i] != '\0'; i++) {
        orig[i] = (char)tolower(orig[i]);
    }
    return orig;
}


void branje(FILE *f, beseda **glava) {
    char buf[MAX];

    while (fscanf(f, "%99[a-zA-Z]%*[^a-zA-Z]", buf) == 1) {
        male(buf);

        //printf("%s\n", buf);
        dodajBesedo(glava, buf);
    }
}


void izpisi(beseda *glava) {
    while (glava != NULL) {
        printf("%s\n", glava->beseda);
        glava = glava->nasl;
    }
}


int poisci(beseda *glava, char *beseda) {
    int n = -1;
    while (glava != NULL && strcmp(glava -> beseda, beseda) != 0) {
        glava = glava -> nasl;

        //printf("%d", n);
        n++;
    }

    if (glava == NULL) {return -1;}
    else {
        return ++n;
    }
}


int povprecnoIskanje(fIsci *isci ,beseda *glava) {
    int sestevek = 0;
    int stevec = 0;

    beseda *temp = glava;
    while (temp != NULL) {
        sestevek += poisci(glava, temp->beseda) +1;
        stevec++;
        //printf("%s %d ", temp->beseda, sestevek);
        temp = temp->nasl;
    }
    //printf("\n sestevek: %d, stevec: %d, rez: %d" ,sestevek, stevec, sestevek/stevec);
    return sestevek/stevec;
}



void dopolniSeznam(beseda *glava) {
    while (glava != NULL) {

        beseda *konec = glava;
        char c = glava->beseda[0];

        while (konec->nasl && konec->nasl->beseda[0] == c) {
            konec = konec->nasl;
        }

        beseda *naslednjaSkupina = konec->nasl;

        for (beseda *p = glava; p != naslednjaSkupina; p = p->nasl) {
            p->nasCrka = naslednjaSkupina;
        }

        glava = naslednjaSkupina;
    }
}

int poisciHitreje(beseda *glava, char *beseda) {
    int n = -1;
    while (glava != NULL && glava->beseda[0] != beseda[0]) {
        glava = glava -> nasCrka;
        n++;
    }
    if (glava == NULL) {return -1;}
    else {
        return ++n;
    }
}


int main(int argc, char *argv[]) {
    FILE *f = fopen("slovenija.txt", "r");


    beseda *glava = NULL;
    branje(f, &glava);
    beseda *celo;
    dopolniSeznam(glava);
    izpisi(glava);

    /*printf("%d\n", poisci(glava, "trb"));
    printf("%d\n", povprecnoIskanje(glava));
    //printf("%d\n", poisciHitreje(glava, "upamo"));*/


    /*fIsci *isci = poisciHitreje;
    printf("Hitreje: %d", isci);
    fIsci *isci2 = poisci;
    printf("Avg: %d", isci2);*/


    while(1) {
        char trb[MAX];
        scanf("%s", trb);
        printf("%d\n", poisci(glava, trb));
        printf("%d\n", poisciHitreje(glava, trb));
    }


    fclose(f);

}
