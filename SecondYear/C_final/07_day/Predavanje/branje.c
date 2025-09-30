//
// Created by Žiga Novak on 30. 9. 25.
//

#define MAX 10
#include <stdio.h>
#include <stdlib.h>

//slaba praksa
char* preberiBesedo() {
    char* beseda = malloc(MAX * sizeof(int));
    scanf("%s", beseda);
    return beseda;
}

//dobra praksa
void preberi(char *besedilo) {
    scanf("%s", besedilo);
}


int main(int argc, char *argv[]) {
    /*printf("Vpisi besedo: ");
    char *beseda = preberiBesedo();
    printf ("Vuhu, beseda je: %s", beseda);
    free(beseda);*/

    char *test = malloc(MAX * sizeof(char));
    printf("test 2: ");
    preberi(test);
    printf("test 2 je %s", test);
    free(test);
}
