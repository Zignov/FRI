//
// Created by Žiga Novak on 29. 9. 25.
//


#include <stdio.h>

void zamenjaj(int *x, int *y) {
    int tmp = *x;
    *x = *y;
    *y = tmp;
}


int main(int argc, char *argv[]) {
    int a = 5;
    int b = 10;

    printf("a: %d, b: %d\n", a, b);

    zamenjaj(&a, &b);
    printf("a: %d, b: %d\n", a, b);

}
