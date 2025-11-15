
#include <stdio.h>

// Main function
int main() {
    int i, n;

    // get the user input ( a number )
    printf("Enter a number: ");
    scanf("%d", &n);

    // Loop through numbers from 1 to n
    for (i = 1; i <= n; i++) {
        // Check if the number is even or odd
        if (i % 2 == 0) {
            // If even, print the number
            printf("%d ", i);
        } else {
            // If odd, print the number in brackets
            printf("[%d] ", i);
        }
    }

    
    return 0;
}
