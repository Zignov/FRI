//
// Created by Žiga Novak on 29. 9. 25.
//

#include <stdio.h>

int main(int argc, char *argv[]) {
    int x = 17;
    //printf("%p\n", &x);

    /* long long naslov;
    printf("vpisite naslov: ");
    printf("%llx", &naslov); */

    int *p;
    p = &x;
    *p = 42;

    //p = (int *) naslov;

    //*p = 42;
    printf("%d\n", x);
}
