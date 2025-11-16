
#include <stdio.h>

// Main function
int main() {
    // Declare a variable to store the input number
    int n;

    // Prompt the user to enter a number
    printf("Enter a number: ");
    scanf("%d", &n);

    // Check if the number is positive or non-positive
    if (n > 0) {
        // If the number is positive, print "Positive"
        printf("Positive");
    } else {
        // If the number is non-positive, print "Non-positive"
        printf("Non-positive");
    }

    // Return 0 to indicate successful execution
    return 0;
}
