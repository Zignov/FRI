//
// Created by Žiga Novak on 25. 9. 25.
//


#include <stdio.h>
#include <stdlib.h>


int main() {
    FILE *vhod = fopen("file.txt", "r");
    FILE *izhod = fopen("output.txt", "w");


    if (vhod == NULL || izhod == NULL) {
        exit(1);
    }


    while (!feof(vhod)) {
        char beseda[100];
        int n = fscanf(vhod, "%s", beseda);
        if (n==1) {
            fprintf(izhod, "%s ", beseda);
        }


    }

    fclose(vhod);
    fclose(izhod);
}
