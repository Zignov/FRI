//
// Created by Žiga Novak on 23. 9. 25.
//

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int main() {
    char najdalsa[100];
    char trenutna[100];

    while (true) {
        fgets(trenutna, 100, stdin);

        if (strlen(najdalsa) < strlen(trenutna)) {
            strcpy(najdalsa, trenutna);
        }
        if (strlen(trenutna) == 1) {
            printf("Najdalsa vrstica je: %s\n", najdalsa);
            break;
        }
    }
}
