//
// Created by Žiga Novak on 23. 9. 25.
//

#include <stdio.h>
#include <stdlib.h>


int main(int argc, char *args[]) {

    int ure, minute, sekunde;

    if (atoi(args[1]) == 1) {
        for (int i = atoi(args[2]); i<atoi(args[3])+1; i++) {

            int trenutna = i;

            ure = trenutna / 3600;
            trenutna -= ure*3600;
            minute = trenutna / 60;
            trenutna-= minute*60;
            sekunde = trenutna;

            printf("%ds = %02d:%02d:%02d\n",i , ure, minute, sekunde);
        }
    }

    if (atoi(args[1]) == 2) {
        //printf("test");

        int trenutna = atoi(args[2]);

        ure = trenutna / 3600;
        trenutna -= ure*3600;
        minute = trenutna / 60;
        trenutna-= minute*60;
        sekunde = trenutna;

        printf("%ds = %02d:%02d:%02d\n",atoi(args[2]) , ure, minute, sekunde);
    }

    if (atoi(args[1]) == 3) {
        //printf("test");
        int ure = atoi(args[2]);
        int minute = atoi(args[3]);
        int sekunde = atoi(args[4]);

        printf("%d ura, %d minut, %d sekund je %d sekund", ure, minute, sekunde, (ure*3600+minute*60+sekunde));
    }
}