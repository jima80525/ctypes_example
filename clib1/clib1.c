#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int func1_no_args(void) {
    static int counter = 0;
    counter++;
    return counter;
}

void func2_string_add_one(char *input) {
    int ii = 0;
    for (; ii < strlen(input); ii++) {
        input[ii]++;
    }
}

char * func3_return_string(void) {
    char* phrase = strdup("I was written in C");
    printf("      C just allocated %p(%ld):  %s\n", phrase, (long int)phrase, phrase);
    return phrase;
}


void func4_free_string(char* ptr) {
    printf("         About to free %p(%ld):  %s\n", ptr, (long int)ptr, ptr);
    free(ptr);
}
