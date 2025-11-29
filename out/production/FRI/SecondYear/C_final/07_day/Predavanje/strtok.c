//
// Created by Žiga Novak on 30. 9. 25.
//


#include <string.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
    char niz[] = "abc:def:ghi";
    char delim[] = ":";

    char *rez;
    rez = strtok(niz, delim);
    while (rez != NULL) {
        printf("%s\n", rez);
        rez = strtok(NULL, delim);

    }
}
