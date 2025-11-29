//
// Created by Žiga Novak on 24. 9. 25.
//

#define W 7
#define H 7
#include <stdio.h>
#include <stdlib.h>


void polje(char polje[H][W]) {
    for (int i = 0; i<H; i++) {
        for (int j = 0; j<W; j++) {
            polje[i][j] = ' ';
        }
    }
}

void izpis(char polje[H][W]) {
    for (int i = 0; i<H; i++) {
        for (int j = 0; j<W; j++) {
            printf("%c", polje[i][j]);
        }
        printf("\n");
    }
}


int poteza(char polje[H][W], int x, int igralec) {
    for (int i = H-1; i>=0; i--) {
        if (polje[i][x] == ' ') {
            if (igralec == 1) {
                polje[i][x] = 'O';
            }
            else {
                polje[i][x] = 'X';
            }

            return 1;
            break;
        }

    }
    return 0;
}


int zmaga(char polje[H][W]) {
    for (int i = 0; i<H; i++) {
        for (int j = 0; j<W-3; j++) {
            if (polje[i][j] != ' ') {
                if (polje[i][j] == polje[i][j+1] && polje[i][j] == polje[i][j+2] && polje[i][j] == polje[i][j+3]) {
                    printf("Zmaga igralec %c\n", polje[i][j]);
                    return 1;
                }
            }
        }
        for (int j = 0; j<W; j++) {
            if (polje[i][j] != ' ') {
                if (polje[i][j] == polje[i+1][j] && polje[i][j] == polje[i+2][j] && polje[i][j] == polje[i+3][j]) {
                    printf("Zmaga igralec %c\n", polje[i][j]);
                    return 1;
                }
            }
        }

        for (int j = 0; j<W; j++) {
            if (polje[i][j] != ' ') {
                if (polje[i][j] == polje[i+1][j+1] && polje[i][j] == polje[i+2][j+2] && polje[i][j] == polje[i+3][j+3]) {
                    printf("Zmaga igralec %c\n", polje[i][j]);
                    return 1;
                }
                else if (polje[i][j] == polje[i+1][j-1] && polje[i][j] == polje[i+2][j-2] && polje[i][j] == polje[i+3][j-3]) {
                    printf("Zmaga igralec %c\n", polje[i][j]);
                    return 1;
                }
                else if (polje[i][j] == polje[i-1][j+1] && polje[i][j] == polje[i-2][j+2] && polje[i][j] == polje[i-3][j+3]) {
                    printf("Zmaga igralec %c\n", polje[i][j]);
                    return 1;
                }
                else if (polje[i][j] == polje[i-1][j-1] && polje[i][j] == polje[i-2][j-2] && polje[i][j] == polje[i-3][j-3]) {
                    printf("Zmaga igralec %c\n", polje[i][j]);
                    return 1;
                }
            }
        }
    }
    return 0;
}





int main() {
    int konec = 0;
    int igralec = 0;
    int temp;
    int input;
    char plosca[H][W];
    int napake[] = {0,0};
    polje(plosca);

    while (konec == 0) {

        printf("Vnesite potezo: ");
        temp = getchar();
        if (temp == '\n') {
            continue;
        }
        input = temp - '0';
        //printf("%d\n", input);
        if (input > 7 || input < 1) {
            printf("Neveljavna poteza\n");
            napake[igralec%2]++;
            if (napake[igralec%2] > 2) {
                konec = 1;
            }
        }
        else {
            if (poteza(plosca, input-1, igralec%2) == 0) {
                napake[igralec%2]++;
                izpis(plosca);
                if (napake[igralec%2] > 2) {
                    konec = 1;
                    printf("Zmaga igralec %d\n", igralec%2+1);
                }
            }
            else {
                izpis(plosca);
                zmaga(plosca);
                igralec++;
            }
        }
    }


}