//
// Created by Žiga Novak on 13. 10. 25.
#include <stdio.h>

int main() {
    // --- scanf(): formatted input from keyboard ---
    int age;
    printf("Enter your age: ");
    scanf("%d", &age);  // reads an integer

    // --- getchar(): reads a single character ---
    char ch;
    printf("Enter a single character: ");
    getchar();          // consume leftover newline from scanf
    ch = getchar();     // reads one character
    printf("You entered: %c\n", ch);

    // --- fgets(): reads a whole line safely (string with spaces) ---
    char name[50];
    printf("Enter your full name: ");
    fgets(name, sizeof(name), stdin);  // reads until newline or buffer full
    printf("Hello, %s", name);

    // --- fscanf(): reads formatted input from a file ---
    FILE *file = fopen("data.txt", "r");
    if (file != NULL) {
        int number;
        fscanf(file, "%d", &number);   // reads an integer from the file
        printf("Number read from file: %d\n", number);
        fclose(file);
    } else {
        printf("Could not open data.txt\n");
    }

    return 0;
}
