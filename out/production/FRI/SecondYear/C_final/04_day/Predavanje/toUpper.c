//
// Created by Žiga Novak on 25. 9. 25.
//


#include <ctype.h>
#include <stdio.h>

int main() {
    FILE *f1 = fopen("file.txt", "r");
    FILE *f2 = fopen("velike.txt", "w");

    int z;
    while ((z = fgetc(f1)) != EOF) {
        z = toupper(z);
        fputc(z, f2);
    }


    fclose(f1);
    fclose(f2);
}
