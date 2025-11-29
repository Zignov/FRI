//
// Created by Žiga Novak on 23. 9. 25.
//

#include <stdio.h>
#include <string.h>
#define N 10

int main() {
    char ime[N];

    printf("Vpisi ime: ");
    scanf("%s", ime); //nizi ne rabjo &

    printf("Pozravljen, %s\n", ime);

    for (int i = strlen(ime)-1; i>=0; i--) {
        putchar(ime[i]);
    }
    putchar('\n');
}