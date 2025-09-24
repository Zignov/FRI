//
// Created by Žiga Novak on 23. 9. 25.
//

#include <stdio.h>
#include <string.h>
#define N 100


int main() {
    char besede[N][50];
    int stevec = 0;
    while (stevec<100) {
        char beseda[50];
        scanf("%s", beseda);

        if (strcmp(beseda, "EOF") == 0) {
            break;
        }
        else {
            strcpy(besede[stevec], beseda);
        }
        stevec++;
    }

    for (int i = stevec-1; i>=0; i--) {
        printf("%s\n", besede[i]);
    }

    //printf("stevilo: %lu", sizeof(besede)/sizeof(besede[0]));

    
}