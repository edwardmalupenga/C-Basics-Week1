#include <stdio.h>

// Function to calculate the average of three numbers
float calculateAverage(float num1, float num2, float num3) {
    return (num1 + num2 + num3) / 3;
}

int main() {
    float num1, num2, num3;

    // getting the user input of enter three numbers
    printf("Enter your first number: ");
    scanf("%f", &num1);
    printf("Enter your second number: ");
    scanf("%f", &num2);
    printf("Enter your third number: ");
    scanf("%f", &num3);

    // Calculating and also displaying the average number
    float average = calculateAverage(num1, num2, num3);
    printf("The average of %.2f, %.2f, and %.2f is: %.2f\n", num1, num2, num3, average);

    return 0;
}
