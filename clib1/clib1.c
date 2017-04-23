
int func1_no_args(void) {
    static int counter = 0;
    counter++;
    return counter;
}
