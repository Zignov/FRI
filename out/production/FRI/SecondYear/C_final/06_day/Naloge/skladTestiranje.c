//
// Created by Žiga Novak on 29. 9. 25.
//

#include <stdio.h>
#define TEKST "0 - konec programa\n1 - dodaj element na sklad\n2 - briši element s sklada\n3 - izpiši vsebino sklada\n4 - zamenjajte sklad\n"
#include "sklad.c"
#include <stdbool.h>


int main(int argc, char *argv[]) {

    printf("Koliko skladov si zelite? ");
    int stSkladov;
    scanf("%d", &stSkladov);
    printf("\n");

    struct sklad skladi[stSkladov];

    for (int i = 0; i < stSkladov; i++) {
        printf("%d. sklad bo velikosti: \n", i+1);
        int velikostSklada;
        scanf("%d", &velikostSklada);

        init(velikostSklada, &skladi[i]);
    }

    struct sklad *trenutni = &skladi[0];

    int c;
    printf(TEKST);

    while (true) {
        scanf("%d", &c);

        switch (c) {
            case 0:
                for (int i = 0; i < stSkladov; i++) {
                    free(skladi[i].tabela);
                }
                exit(0);
                break;
            case 1:
                printf("Vnesite stevilo\n");
                int stevilo;
                scanf("%d", &stevilo);
                push(stevilo, trenutni);
                break;

            case 2:
                pop(trenutni);
                break;

            case 3:
                printf("kaz: %d\n", trenutni -> kazalec);
                if (!isEmpty(trenutni)) {
                    for (int i = 0; i <= trenutni -> kazalec; i++) {
                        printf("%d", trenutni -> tabela[i]);
                    }
                    printf("\n");
                }
                break;

            case 4:
                printf("kateri sklad zelite? ");
                int menjava;
                scanf("%d", &menjava);
                trenutni = &skladi[menjava-1];
        }

        printf(TEKST);
    }
}
