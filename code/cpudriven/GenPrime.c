void generatePrimenumbers(int n) {
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
        }
    }
}

int main() {
    generatePrimenumbers(50000);
}
