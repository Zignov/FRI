//
// Created by Žiga Novak on 2. 10. 25.
//


#include <stdio.h>
#include <stdlib.h>

#pragma pack(1)
typedef struct Win1xHeader
{
    char* Type;          /* File type identifier (always 0) */
    char* Width;         /* Width of the bitmap in pixels */
    char* Height;        /* Height of the bitmap in scan lines */
    char* ByteWidth;     /* Width of bitmap in bytes */
    int Planes;        /* Number of color planes */
    int BitsPerPixel;  /* Number of bits per pixel */
} WIN1XHEADER;

#define N 2048

int main(int argc, char *argv[]) {

    FILE *vhod = fopen(argv[1], "rb");
    FILE *izhod = fopen(argv[2], "wb");


    if (vhod == NULL || izhod == NULL) {
        exit(1);
    }

    int buf[N];
    char zac[50];
    int stevec = 0;


    stevec = fread(zac, sizeof(int), 50, vhod);



    printf("header: %s" , zac);


    do {
        stevec = fread(buf, sizeof(int), N, vhod);
        fwrite(buf, sizeof(int), stevec, izhod);
    }
    while (stevec>0);
}
