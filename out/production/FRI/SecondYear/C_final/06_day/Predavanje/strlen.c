//
// Created by Žiga Novak on 29. 9. 25.
//


#include <stdio.h>

int strlen1(char niz[]) {
    int i = 0;
    while (niz[i] != '\0') i++;
    return i;
}

int strlen2(char *niz) {
    int i = 0;
    while (*niz != '\0') {
        niz++; i++;
    }
    return i;
}


int main() {
    char niz[] = "ponedeljek";
    printf("Dolzina (strlen1): %d\n", strlen1(niz));
    printf("Dolzina (strlen2): %d\n", strlen2(niz));

}