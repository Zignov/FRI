//
// Created by Žiga Novak on 23. 9. 25.
//

//Podan interval, prebere stevilo, pove ce zadanes


#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    int a, b, x;

    printf("Vpisi spodnjo mejo: ");
    scanf("%d", &a);

    printf("Vpisi zgornjo mejo: ");
    scanf("%d", &b);

    printf("Ugibaj... ");
    scanf("%d", &x);

    int rnd;
    srand(time(NULL));
    rnd = rand();
    rnd = a + rnd % (b - a + 1);

    if (rnd == x) {
        printf("Bravo \n");
    }
    else {
        printf("Noup, bilo je %d", rnd);
    }

}