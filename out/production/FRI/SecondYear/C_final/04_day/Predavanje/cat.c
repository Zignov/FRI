//
// Created by Žiga Novak on 25. 9. 25.
//

#include <stdio.h>

void cat(FILE *vhod) {
    char vrstica[100];
    while (!feof(vhod)) {
        fgets(vrstica, 100, vhod);
        printf("%s", vrstica);
    }

}


int main(int argc, char *args[]) {
    if (argc == 1) {
        cat(stdin);
    }
    else {
        FILE *f = fopen(args[1], "r");
        cat(f);
        fclose(f);
    }

}