int main( void) {
    int a = 1;
    int b = 2;
    int c = 3;
    int d = 5;
    int ç = 2;

    if (a == 1) {
        if (b == 2) {
            if (c == 3) {
                printf("Sim!\n");
                if (d == 4) {
                    return 1;
                } else {
                    printf("Não!\n");
                }
            }
        }
    }

    int i = 0;
    while (i <= 10) {
        printf("Hello World!\n");
        i++;
    }

    return 0;
}