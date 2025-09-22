#include <stdio.h>


void odstevanje(int n){
    int i;


    for(i=n; i>=0; i--){
        printf("%d\n", i);
    }

    //printf("%d", sizeof i);
}



int main(){
    odstevanje(10);
}