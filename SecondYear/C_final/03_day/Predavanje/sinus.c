//
// Created by Žiga Novak on 24. 9. 25.
//

#define W 80
#define H 25
#include <stdio.h>
#include <math.h>

char zaslon[H][W];

void clear() {
    for (int i = 0; i<H; i++) {
        for (int j = 0; j<W; j++) {
            zaslon[i][j] = ' ';
        }
    }
}

void izpisi() {
    for (int i = 0; i<H; i++) {
        for (int j = 0; j<W; j++) {
            printf("%c", zaslon[i][j]);
        }
        printf("\n");
    }
}


void koordinatniSistem(){
    for (int j = 0; j<W; j++) {
        zaslon[H/2][j] = '-';
    }
    for (int i = 0; i<H; i++) {
        zaslon[i][W/2] = '|';
    }

    zaslon[H/2][W/2] = '+';
    }


void graf() {
    double x1 = -3.14;
    double x2 = 3.14;
    double y1 = -1;
    double y2 = 1;

    for (int j = 0; j<W; j++) {
        double x = j * (x2 - x1) / (W-1) + x1;
        double y = sin(x);
        int i  = (H-1) * (y - y1) / (y2 - y1);
        zaslon[i][j] = '*';
    }
}


int main() {
    clear();
    koordinatniSistem();
    graf();
    izpisi();
}