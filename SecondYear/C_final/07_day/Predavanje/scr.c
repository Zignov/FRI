//
// Created by Žiga Novak on 30. 9. 25.
//


#include <stdio.h>
#include <string.h>


int main(int argc, char *argv[]) {
    char *niz = "Beseda v amlo daljsem nizu";

    char *nasel = strstr(niz, " ");
    --nasel;
    while ( nasel >= niz) {
        printf("%c", *nasel);
        nasel--;
    }


    printf("\n");
    char *zacetek = niz;
    while (strlen(zacetek)>0) {
        char *presledek = strstr(niz, " ");
        while (zacetek < presledek) {
            printf("%c", *zacetek);
            zacetek++;
        }
        zacetek++;
    }
}
