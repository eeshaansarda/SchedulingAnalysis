// #include "Ackermann.h"

int ackermannFunction(int m, int n) {
    if(m == 0) {
        return n + 1;
    } else if((m > 0) && n == 0) {
        return ackermannFunction(m-1, 1);
    } else if((m > 0) && (n > 0)){
        return ackermannFunction(m-1, ackermannFunction(m, n-1));
    }
}

int main() {
    ackermannFunction(4, 2);
}
