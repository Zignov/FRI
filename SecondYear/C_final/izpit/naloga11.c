//
// Created by Žiga Novak on 13. 10. 25.
//
#define N 50
#include <stdlib.h>
#include <stdio.h>

int prestejBite(int st) {
    int biti = 0;

    while (st>0) {
        if ((st & 1) != 0) {
            biti++;
        }
        st=st>>1;
    }
    return biti;
}

int primerjaj(const void *a, const void *b) {
    return (*(int *)a - *(int *)b);
}

void izpisiSeznam(int seznam[], int velikost) {
    if (velikost <=0) {
        return;
    }
    qsort(seznam, velikost, sizeof(int), primerjaj);

    for (int i = 0; i<velikost; i++) {
        printf("%d ", seznam[i]);
    }
    printf("\n");
}


int main() {

    int stevec = 1;

    //printf("%d", prestejBite(95));
    int seznam1[N], seznam2[N], seznam3[N], seznam4[N], seznam5[N], seznam6[N];
    int st1 = 0, st2 = 0, st3 = 0, st4 = 0, st5 = 0, st6 = 0;

    while (stevec<100) {


        switch (prestejBite(stevec)) {
            case 1:
                seznam1[st1] = stevec;
                st1++;
                break;
            case 2:
                seznam2[st2] = stevec;
                st2++;
                break;
            case 3:
                seznam3[st3] = stevec;
                st3++;
                break;
            case 4:
                seznam4[st4] = stevec;
                st4++;
                break;
            case 5:
                seznam5[st5] = stevec;
                st5++;
                break;
            case 6:
                seznam6[st6] = stevec;
                st6++;
                break;
        }
        //printf("stevec: %d", stevec);
        stevec++;
    }


        printf("1:\n\t");
        izpisiSeznam(seznam1, st1);
        printf("2:\n\t");
        izpisiSeznam(seznam2, st2);
        printf("3:\n\t");
        izpisiSeznam(seznam3, st3);
        printf("4:\n\t");
        izpisiSeznam(seznam4, st4);
        printf("5:\n\t");
        izpisiSeznam(seznam5, st5);
        printf("6:\n\t");
        izpisiSeznam(seznam6, st6);

}