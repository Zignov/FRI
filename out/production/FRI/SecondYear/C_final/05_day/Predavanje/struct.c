//
// Created by Žiga Novak on 26. 9. 25.
//

#define MAX 20
#include <stdio.h>
#define N 2

struct oseba {
    char ime[MAX];
    char priimek[MAX];
    int starost;
};


int main(int argc, char *argv[]) {
    struct oseba o[N];

    for (int i = 0; i<N; i++) {
        printf("Vpisi ime: ");
        scanf("%s", o[i].ime);

        printf("Vpisi priimek: ");
        scanf("%s", o[i].priimek);

        printf("Vpisi starost: ");
        scanf("%d", &o[i].starost);

        printf("Pozdravljen %s %s, star si: %d\n", o[i].ime, o[i].priimek, o[i].starost);
    }
}
