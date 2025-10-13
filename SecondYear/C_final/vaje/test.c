//
// Created by Žiga Novak on 13. 10. 25.
//


#include<stdlib.h>

int rekurzija(int num, int dolzina){
    int stevec = 0;
    char x [20] = itoa(num);
    for(int i = 0; i<dolzina; i++){
        stevec += atoi(x[i]);
    }
    return stevec;
}

int addDigits(int num) {
    int rez=0;

    do{
        rez = rekurzija(num, strlen(itoa(num)));
    }
    while(rez>=10);
}