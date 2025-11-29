//
// Created by Žiga Novak on 24. 9. 25.
//

#include <stdio.h>
#include <string.h>


void kodiraj(char vhod[], char kljuc[], int dolzina) {

    char izhod[strlen(vhod)];

    for (int i = 0; i<dolzina; i++) {
        char crka = vhod[i];
        char k = kljuc[i%strlen(kljuc)];

        char code = (crka ^ k);

        printf("code: %c\n", code);
        printf("k: %c\n", k);
        izhod[i] = code;
    }

    strcpy(vhod, izhod);
}
