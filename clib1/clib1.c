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
    char* name = strdup("I was written in C");
    return name;
}
