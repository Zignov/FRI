//
// Created by Žiga Novak on 25. 9. 25.
//


#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        exit(1);
    }


    FILE *f = fopen(argv[1], "r");
    int crka;
    int vrstice = 0;
    int besede = 0;
    int znakov = 0;
    int podvojitev = 0;

    while ((crka = fgetc(f)) != EOF) {
        if (crka == '\n') {
            vrstice++;
        }

        if ( crka == ' ' || crka == '\n' || crka == '\t') {
            podvojitev = 0;
        }
        else {
            if (!podvojitev) {
                besede++;
                podvojitev = 1;
            }
            //printf("%c", crka
        }

        znakov++;
    }

    printf("%d %d %d", vrstice, besede, znakov);

    fclose(f);

}
