#include <stdio.h>

void generatePrimenumbersAndWrite(int n, FILE *f) {
    for(int i = 2; i <= n; i++) {
        int c = 0;
        for(int j = 1; j <= i; j++) {
            if(i%j == 0) {
                c++;
            }
        }

        if(c == 2) {
            // is prime
            // printf("%d ",i); // is a system call
            fprintf(f, "%d ", i);
        }
    }
}

int main() {
    FILE *f;
    for(int i = 0; i < 800; i++) {
        f = fopen("./cpu&iodriven/text/primeNumbers.txt", "w");
        generatePrimenumbersAndWrite(1300, f);
        fclose(f);
    }
}
