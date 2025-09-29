//
// Created by Žiga Novak on 29. 9. 25.
//

#include <stdio.h>

int main() {
    char a[] = {'a', 'b', 'c', 'd', 'e'};

    char *pa;
    pa = &a[0];
    *pa = 'z';

    *(pa+2) = '@';

    /*pa++;
    pa++;
    pa++;

    *pa = 'l';*/

    pa[3] = '3';


    for (int i = 0; i < sizeof(a); i++) {
        printf("%c ", a[i]);
        printf("\n");
    }

}
