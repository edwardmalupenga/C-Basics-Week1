#include <stdio.h>

int main() {
    char name[100];
    int age;
    char hobby[100];

    // Ask user for their name
    printf("Enter your name: ");
    scanf("%99[^\n]", name); // Reads until newline (includes spaces)
    getchar(); // Consume the leftover newline character
    
    // Ask user for their age
    printf("Enter your age: ");
    scanf("%d", &age);
    getchar(); // Consume the leftover newline character
    
    // Ask user for their hobby
    printf("Enter your favorite hobby: ");
    scanf("%99[^\n]", hobby); // Reads until newline (includes spaces)

    // Print user's information
    printf("\nHello, my name is %s.\n", name);
    printf("I am %d years old.\n", age);
    printf("My favorite hobby is %s.\n", hobby);

    // Print greeting message
    printf("\nHello, %s! You are %d years old and enjoy %s.\n", name, age, hobby);

    return 0;
}
