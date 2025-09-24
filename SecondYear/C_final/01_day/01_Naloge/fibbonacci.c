#include <stdio.h>
#include <stdlib.h>


int main(int argc, char *args[]){

    if(argc != 2){
        printf("Napaka!");
    }

    else{

        int overflow = 0;
        int vsota = 2;
        int stevec = atoi(args[1]);
        int x = 1;
        int y = 1;

        
        for (int i = 3; i<=stevec; i++){
            
            int zacasna = x;
            x+= y;
            y = zacasna;

            vsota += x;

            if(vsota<0){
                overflow = 1;
                break;
            }
            //printf("Fib: %d, sestevek: %d\n", x, vsota);
            
        }

        if(overflow == 1){
            printf("Napaka!\n");
        }
        else{
            printf("sesetevek = %d\n", vsota);
        }

        

    }


}