
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(){
    srand(time(NULL));

    for(int i = 0; i<10; i++){
        int x  = rand();
        printf("%d\n", x);
    }
}