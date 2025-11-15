#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h> 

// --- Configuration Constants & Data Model ---
#define MAX_ACCOUNTS 100        // Maximum accounts supported by the system
#define MAX_NAME_LEN 50
#define MAX_PASS_LEN 20
#define MAX_PHONE_LEN 15        // Added phone number length
#define FILENAME "bank_data.txt" // File for persistent storage

// Define the Bank Account Structure (the core data unit)
typedef struct {
    char fullName[MAX_NAME_LEN];
    long accountNumber; 
    char password[MAX_PASS_LEN]; 
    double balance;     
    char phoneNumber[MAX_PHONE_LEN]; // New field for user contact
} Account;

// --- Global System State ---
Account accounts[MAX_ACCOUNTS]; // The main array holding all active accounts
int accountCount = 0;          // How many accounts are currently registered
int loggedInAccountIndex = -1; // The index of the active user, -1 if no one is logged in


// Simple utility to find an account index by number
int findAccountIndex(long accNum) {
    // Loop through the array until a match is found
    for (int i = 0; i < accountCount; i++) {
        if (accounts[i].accountNumber == accNum) {
            return i; // Found it! Return the position.
        }
    }
    return -1; // No account found with that number
}

// --- Bonus Feature: File I/O ---

// Startup function: Try to read data from the file
void loadAccounts() {
    FILE *file = fopen(FILENAME, "r");
    if (file == NULL) {
        printf("\n[SYS] No 'bank_data.txt' found. Starting fresh.\n");
        accountCount = 0;
        return;
    }

    accountCount = 0;
    // Format: fullName accountNumber password balance phoneNumber
    // We expect 5 pieces of data for each account
    while (accountCount < MAX_ACCOUNTS && 
           fscanf(file, "%s %ld %s %lf %s", 
                  accounts[accountCount].fullName, 
                  &accounts[accountCount].accountNumber,
                  accounts[accountCount].password, 
                  &accounts[accountCount].balance,
                  accounts[accountCount].phoneNumber) == 5) { 
        accountCount++;
    }

    fclose(file);
    printf("\n[SYS] Loaded %d existing accounts.\n", accountCount);
}

// Saves current data back to the file
void saveAccounts() {
    FILE *file = fopen(FILENAME, "w");
    if (file == NULL) {
        fprintf(stderr, "\n[ERROR] CRITICAL: Failed to open %s for saving!\n", FILENAME);
        return;
    }

    // Write all currently loaded accounts back to the file
    for (int i = 0; i < accountCount; i++) {
        fprintf(file, "%s %ld %s %.2f %s\n", 
                accounts[i].fullName, 
                accounts[i].accountNumber,
                accounts[i].password, 
                accounts[i].balance,
                accounts[i].phoneNumber);
    }

    fclose(file);
    // printf("\n[SYS] Data saved successfully.\n"); // Keep silent unless needed for debugging
}

// --- REQUIRED FEATURE 1: USER REGISTRATION ---
void registerAccount() {
    if (accountCount >= MAX_ACCOUNTS) {
        printf("\n[ERROR] Sorry, the bank is full. We reached the account limit.\n");
        return;
    }

    printf("\n*** NEW ACCOUNT SETUP ***\n");

    long accNum;
    int index;
    
    // Step 1: Get Account Number, ensuring it's unique and formatted correctly.
    do {
        printf("1. Enter a unique 6-digit Account Number (e.g., 100001): ");
        if (scanf("%ld", &accNum) != 1 || accNum < 100000 || accNum > 999999) {
            printf("[Validation] Account number must be a 6-digit number.\n");
            // Important: clear the input buffer after bad input
            while (getchar() != '\n'); 
            accNum = 0; 
            continue;
        }
        index = findAccountIndex(accNum);
        if (index != -1) {
            printf("[Validation] That account number already exists. Try again.\n");
        }
    } while (index != -1);
    
    // Assign the new account number to the next slot
    accounts[accountCount].accountNumber = accNum;
    
    // Clear buffer after number input, before string input
    while (getchar() != '\n'); 

    // Step 2: Get Name
    printf("2. Enter Full Name (no spaces, e.g., JohnDoe): ");
    scanf("%s", accounts[accountCount].fullName); 
    
    // Step 3: Get Phone Number (as requested)
    printf("3. Enter Phone Number (no spaces, e.g., 555-1234): ");
    scanf("%s", accounts[accountCount].phoneNumber);

    // Step 4: Get Password (the user's 'new password' for this account)
    printf("4. Create Password (max %d chars): ", MAX_PASS_LEN - 1);
    scanf("%s", accounts[accountCount].password);

    // Step 5: Initial Deposit
    double deposit;
    do {
        printf("5. Enter Initial Deposit Amount (must be >= ZMW 10.00): ZMW ");
        if (scanf("%lf", &deposit) != 1 || deposit < 10.00) {
            printf("[Validation] Invalid deposit amount.\n");
            while (getchar() != '\n');
            deposit = 0.0;
        }
    } while (deposit < 10.00);
    
    accounts[accountCount].balance = deposit;

    // Finalize and save
    accountCount++;
    saveAccounts(); 

    printf("\n[SUCCESS] Welcome, %s! Your account is ready.\n", accounts[accountCount-1].fullName);
    printf("Account: %ld | Phone: %s\n", accNum, accounts[accountCount-1].phoneNumber);
}

// --- BONUS FEATURE: LOGIN SYSTEM ---
int authenticateUser() {
    long accNum;
    char passInput[MAX_PASS_LEN];
    int index;

    printf("\n*** LOGIN AUTHENTICATION ***\n");

    printf("Account Number: ");
    if (scanf("%ld", &accNum) != 1) {
        printf("[ERROR] Invalid input. Please enter a number.\n");
        while (getchar() != '\n'); 
        return 0;
    }

    printf("Password: ");
    scanf("%s", passInput);

    index = findAccountIndex(accNum);

    // Check if account exists AND password matches
    if (index != -1 && strcmp(accounts[index].password, passInput) == 0) {
        loggedInAccountIndex = index;
        printf("\n[SUCCESS] Login successful. Hello, %s.\n", accounts[index].fullName);
        return 1;
    } else {
        printf("\n[ERROR] Login failed: Account or password incorrect.\n");
        return 0;
    }
}

// --- REQUIRED FEATURE 6: DISPLAY ACCOUNT DETAILS ---
void displayDetails() {
    if (loggedInAccountIndex == -1) return; 

    int current_index = loggedInAccountIndex;
    printf("\n=== Your Account Overview ===\n");
    printf("Holder:         %s\n", accounts[current_index].fullName);
    printf("Account Number: %ld\n", accounts[current_index].accountNumber);
    printf("Phone Number:   %s\n", accounts[current_index].phoneNumber);
    printf("Current Balance: ZMW %.2f\n", accounts[current_index].balance);
    printf("Security:       Password hash is hidden from view.\n"); 
    printf("=============================\n");
}

// --- REQUIRED FEATURE 2: FUND DEPOSIT ---
void depositFunds() {
    if (loggedInAccountIndex == -1) return;

    double amount;
    int current_index = loggedInAccountIndex;

    printf("\n*** Cash Deposit ***\n");
    printf("Current Balance: ZMW %.2f\n", accounts[current_index].balance);
    
    printf("Enter deposit amount: ZMW ");
    // Validate that the input is a positive number
    if (scanf("%lf", &amount) != 1 || amount <= 0) {
        printf("[Validation] Deposit must be a positive number.\n");
        while (getchar() != '\n');
        return;
    }

    // Update and save the data
    accounts[current_index].balance += amount;
    saveAccounts();

    printf("\n[SUCCESS] ZMW %.2f added.\n", amount);
    printf("NEW Balance: ZMW %.2f\n", accounts[current_index].balance);
}

// --- REQUIRED FEATURE 3: FUND WITHDRAWAL ---
void withdrawFunds() {
    if (loggedInAccountIndex == -1) return;

    double amount;
    int current_index = loggedInAccountIndex;

    printf("\n*** Cash Withdrawal ***\n");
    printf("Current Balance: ZMW %.2f\n", accounts[current_index].balance);

    printf("Enter withdrawal amount: ZMW ");
    if (scanf("%lf", &amount) != 1 || amount <= 0) {
        printf("[Validation] Withdrawal must be a positive number.\n");
        while (getchar() != '\n');
        return;
    }

    // Check for insufficient funds (the core logic here)
    if (accounts[current_index].balance >= amount) {
        accounts[current_index].balance -= amount;
        saveAccounts();
        
        printf("\n[SUCCESS] ZMW %.2f dispensed.\n", amount);
        printf("NEW Balance: ZMW %.2f\n", accounts[current_index].balance);
    } else {
        printf("\n[ERROR] Insufficient funds! You only have ZMW %.2f available.\n", accounts[current_index].balance);
    }
}

// --- REQUIRED FEATURE 4: ONLINE FUND TRANSFER ---
void transferFunds() {
    if (loggedInAccountIndex == -1) return;

    long recipientAccNum;
    double amount;
    int senderIdx = loggedInAccountIndex;
    int recipientIdx;

    printf("\n*** Account to Account Transfer ***\n");
    printf("Your Balance: ZMW %.2f\n", accounts[senderIdx].balance);

    // 1. Get recipient
    printf("Enter Recipient Account Number: ");
    if (scanf("%ld", &recipientAccNum) != 1) {
        printf("[ERROR] Invalid account number format.\n");
        while (getchar() != '\n');
        return;
    }

    recipientIdx = findAccountIndex(recipientAccNum);
    if (recipientIdx == -1) {
        printf("[ERROR] Recipient account %ld not found in the system.\n", recipientAccNum);
        return;
    }

    // Prevent transferring to self
    if (senderIdx == recipientIdx) {
        printf("[ERROR] Please use Deposit/Withdrawal for self-account operations.\n");
        return;
    }
    
    // 2. Get amount
    printf("Enter transfer amount: ZMW ");
    if (scanf("%lf", &amount) != 1 || amount <= 0) {
        printf("[Validation] Transfer amount must be positive.\n");
        while (getchar() != '\n');
        return;
    }
    
    // 3. Final validation and processing
    if (accounts[senderIdx].balance >= amount) {
        // Debit sender, Credit recipient
        accounts[senderIdx].balance -= amount;
        accounts[recipientIdx].balance += amount;
        saveAccounts();

        printf("\n[SUCCESS] Transferred ZMW %.2f to %s (Acc: %ld).\n", 
               amount, accounts[recipientIdx].fullName, accounts[recipientIdx].accountNumber);
        printf("Your New Balance: ZMW %.2f\n", accounts[senderIdx].balance);
    } else {
        printf("\n[ERROR] Insufficient funds for this transfer.\n");
    }
}

// --- REQUIRED FEATURE 5: CHANGE PASSWORD ---
void changePassword() {
    if (loggedInAccountIndex == -1) return;

    char oldPass[MAX_PASS_LEN];
    char newPass1[MAX_PASS_LEN];
    char newPass2[MAX_PASS_LEN];
    int current_index = loggedInAccountIndex;

    printf("\n*** Password Reset ***\n");
    
    // Verification check first
    printf("1. Enter Current Password for verification: ");
    scanf("%s", oldPass);

    if (strcmp(accounts[current_index].password, oldPass) != 0) {
        printf("[ERROR] Current password incorrect. Aborting change.\n");
        return;
    }

    // Get new password and confirmation
    printf("2. Enter New Password: ");
    scanf("%s", newPass1);
    
    printf("3. Confirm New Password: ");
    scanf("%s", newPass2);

    if (strcmp(newPass1, newPass2) == 0) {
        // If they match, apply the change
        strcpy(accounts[current_index].password, newPass1);
        saveAccounts();
        printf("\n[SUCCESS] Password updated for account %ld.\n", accounts[current_index].accountNumber);
    } else {
        printf("[ERROR] New passwords did not match. No changes made.\n");
    }
}

// --- MENU DISPLAY FUNCTIONS ---

void displayPreLoginMenu() {
    printf("\n\n==================================\n");
    printf("   ONLINE BANKING SYSTEM \n");
    printf("==================================\n");
    printf("1. Register New Account\n");
    printf("2. Login to Account\n");
    printf("0. Exit Application\n");
    printf("----------------------------------\n");
    printf("What do you want to do? (Enter number): ");
}

void displayLoggedInMenu() {
    printf("\n\n=== Welcome back, %s! ===\n", accounts[loggedInAccountIndex].fullName);
    printf("Account: %ld | Balance: ZMW %.2f\n", accounts[loggedInAccountIndex].accountNumber, accounts[loggedInAccountIndex].balance);
    printf("==================================\n");
    printf("1. Deposit Cash\n");
    printf("2. Withdraw Cash\n");
    printf("3. Transfer Money to another Account\n");
    printf("4. Change My Password\n");
    printf("5. Show Account Details\n");
    printf("0. Logout\n");
    printf("----------------------------------\n");
    printf("What do you want to do? (Enter number): ");
}

// --- MAIN PROGRAM ENTRY POINT ---

int main() {
    loadAccounts(); // Try to load data first

    int choice;
    int running = 1;

    // Main application loop
    while (running) {
        if (loggedInAccountIndex == -1) {
            // State 1: User is logged out
            displayPreLoginMenu();
            if (scanf("%d", &choice) != 1) {
                printf("[ERROR] Invalid choice. Please enter a number.\n");
                while (getchar() != '\n'); 
                continue;
            }

            switch (choice) {
                case 1: 
                    registerAccount(); // Go through registration
                    break;
                case 2: 
                    authenticateUser(); // Attempt login
                    break;
                case 0: 
                    printf("\nSystem shutting down. Goodbye! 🚀\n");
                    running = 0;
                    break;
                default: 
                    printf("\n[ERROR] Command not recognized. Try again.\n");
            }
        } else {
            // State 2: User is logged in
            displayLoggedInMenu();
            if (scanf("%d", &choice) != 1) {
                printf("[ERROR] Invalid choice. Please enter a number.\n");
                while (getchar() != '\n'); 
                continue;
            }

            switch (choice) {
                case 1: depositFunds(); break;
                case 2: withdrawFunds(); break;
                case 3: transferFunds(); break;
                case 4: changePassword(); break;
                case 5: displayDetails(); break;
                case 0: 
                    loggedInAccountIndex = -1; // Set index to -1 to return to logged out state
                    printf("\n[SUCCESS] You have successfully logged out.\n");
                    break;
                default: 
                    printf("\n[ERROR] Command not recognized. Try again.\n");
            }
        }
    }

    return 0;
}