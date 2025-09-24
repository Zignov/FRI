#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *args[]){



    if(argc != 4){
        printf("Napaka\n");
    }
    else{

        int n = atoi(args[1]);
        int m = atoi(args[3]);

        //printf("%d", n);

        for (int i = 0; i<n; i++){

            for(int j = 0; j<m*i; j++){
                printf(".");
            }
            printf("Pozdravljen, %s\n", args[2]);
        }
    }


}