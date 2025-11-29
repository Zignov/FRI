//
// Created by Žiga Novak on 1. 10. 25.
//


#include <cstdio>
#include <cstdlib>
#include <cstring>
#define MAX 10

typedef struct student {
    int id;
    char *ime;
    int *ocene;
    int st_ocen;

    struct student *next;

}student;

student* novStudent(int id, char *ime) {
    student *n;
    n = (student*) malloc(sizeof(student));


    n->id = id;
    //n->ime = (char*)malloc(strlen(ime) * sizeof(char));
    n -> ocene = (int*)malloc(MAX * sizeof(int));
    n -> st_ocen = 0;
    n -> ime = strdup(ime);

    return n;
}

void izpisi(student *s) {
    printf("Ime: %s, id: %d, ocene: \n", s->ime, s->id);

    for (int i = 0; i < s->st_ocen; i++) {
        printf("%d ", s->ocene[i]);
    }
    printf("\n");
}


void dodajOcene(student *s, int ocena) {
    s->ocene[s->st_ocen++] = ocena;
}

void freeStudent(student *s) {
    free(s->ocene);
    free(s->ime);
    free(s);
}


student *dodajZ(student *z, student *n) {
    n -> next = z;
    return n;
}

student * dodajK(student *z, student *n) {
    if (z == NULL) {
        return n;
    }

    student *t = z;
    while (t->next != NULL) {
        t = t ->next;
    }

    t->next = n;
    return z;
}


student * dodajU(student *z, student *n) {
    if (z == NULL || z->id >= n->id) {
        return dodajZ(z, n);
    }

    student *t = z;
    while (t->next != NULL && t->next->id < n->id) {
        t = t -> next;
    }
    n->next = t->next;
    t->next = n;
}

void izpisiZ(student *z) {
    student *t = z;
    while (t != NULL) {
        izpisi(t);
        t = t->next;
    }
}


student * brisiElement(student *z, int id) {
    if (z == NULL) return NULL;
    if (z->id == id) {
        student *tmp = z;
        z = z->next;

        freeStudent(tmp);
        return z;
    }

    student *t = z;
    while (t->next != NULL && t->next->id != id)
        t = t->next;

        if (t->next != NULL) {
            student *tmp = t->next;
            t->next = t->next->next;
            freeStudent(tmp);
        }
    return z;
}

int main(int argc, char *argv[]) {
    student *s1 = novStudent(1, "Ivan");
    student *s2 = novStudent(9, "Jan");
    student *s3 = novStudent(6, "Rok");
    student *s4 = novStudent(1, "Tea");
    student *s5 = novStudent(5, "Mika");


    student *z = NULL;

    z = dodajK(z, s2);
    z = dodajK(z, s3);
    z = dodajK(z, s1);
    z = dodajK(z, s4);

    brisiElement(z, 6);


    dodajOcene(s1, 10); dodajOcene(s1, 9);
    //izpisi(s1);
    izpisiZ(z);

    freeStudent(s1);
}
