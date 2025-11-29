//
// Created by Žiga Novak on 24. 9. 25.
//

#include <stdio.h>
#include <string.h>

void kodiraj(char[], char[], int);

int main() {
    char kljuc[10];
    char vhod[10];

    printf("Vpisi besedilo: ");
    scanf("%s", vhod);

    printf("Vpisi kljuc: ");
    scanf("%s", kljuc);

    int len = strlen(vhod);
    kodiraj(vhod, kljuc, len);
    printf("Zakodirano besedilo: %s\n", vhod);
}