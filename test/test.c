#include <stdio.h>
#include <stdlib.h>

int main(){
    printf("hello\n");

    int res = 0;
    for(int i = 1; i <= 100; i++){
        res += i;
    }
    printf("%d\n", res);
}