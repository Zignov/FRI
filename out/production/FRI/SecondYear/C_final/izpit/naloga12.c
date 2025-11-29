//
// Created by Žiga Novak on 13. 10. 25.
//
#include <ctype.h>
#include<stdio.h>
#include<stdlib.h>
#include <string.h>

char* vPapajscino(char *niz) {
    int dolzina = strlen(niz);
    int stevec = 0;

    for (int i = 0; i < dolzina; i++) {
        char crka = tolower(niz[i]);
        if (crka == 'a' || crka == 'e' || crka == 'i' || crka == 'o' || crka == 'u'){
            stevec++;
        }
    }

    char* rez = malloc(stevec * sizeof(char));

    for (int i = 0, j = 0; i < dolzina; i++, j++) {
        char crka = niz[i];
        rez[j] = crka;
        crka = tolower(crka);
        if (crka == 'a' || crka == 'e' || crka == 'i' || crka == 'o' || crka == 'u'){
            rez[j+1] = 'p';
            rez[j+2] = tolower(crka);
            j+=2;
        }
    }

    return rez;
}


int main(int argc, char **args) {
    char niz[] = "Ali je res?";
    printf("%s\n", vPapajscino(niz));
    return 0;
}