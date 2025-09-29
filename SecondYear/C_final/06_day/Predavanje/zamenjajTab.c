//
// Created by Žiga Novak on 29. 9. 25.
//

#include <stdio.h>

void zamenjaj(int a[], int i, int j) {
    int t = a[i];
    a[i] = a[j];
    a[j] = t;
}

int main() {
    int tab[5] = {0,1,2,3,4};

    // izpišemo drugi in četrti element
    printf("tab[2]=%d, tab[4]=%d \n", tab[2], tab[4]);

    // zamenjamo vrednost?
    zamenjaj(tab, 2, 4);

    // izpišemo drugi in četrti element
    printf("tab[2]=%d, tab[4]=%d \n", tab[2], tab[4]);
}
