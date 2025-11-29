//
// Created by Žiga Novak on 24. 9. 25.
//

#include <string.h>
#include <stdio.h>

int string2int(char stevilo[]) {
    int vsota = 0;

    for (int i = 0; strlen(stevilo) > i; i++) {
        int stevka = stevilo[i] - '0';
        vsota = vsota*10 + stevka;
    }


    return vsota;
}

int main() {
    char stevilo[10];
    printf("Vpissi stevilo: ");
    scanf("%s", stevilo);

    int vrednost = string2int(stevilo);
    printf("Vrednost je %d\n", vrednost);
}
