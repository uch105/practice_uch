#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <termios.h>
#include <sys/stat.h>

#define MAX_ENTRIES 50
#define MAX_LENGTH 100
#define CONFIG_FILE ".ssh_manager_config"

// Color definitions
#define COLOR_RED     "\x1b[31m"
#define COLOR_GREEN   "\x1b[32m"
#define COLOR_YELLOW  "\x1b[33m"
#define COLOR_BLUE    "\x1b[34m"
#define COLOR_MAGENTA "\x1b[35m"
#define COLOR_CYAN    "\x1b[36m"
#define COLOR_RESET   "\x1b[0m"

typedef struct {
    char username[MAX_LENGTH];
    char ip[MAX_LENGTH];
    char description[MAX_LENGTH];
    char keyfile[MAX_LENGTH];
    int port;
    int use_password;
} SSHServer;

SSHServer servers[MAX_ENTRIES];
int serverCount = 0;

// Function to get password without echo
void getPassword(char *password, size_t max) {
    struct termios oldterm, newterm;
    tcgetattr(STDIN_FILENO, &oldterm);
    newterm = oldterm;
    newterm.c_lflag &= ~(ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newterm);
    
    fgets(password, max, stdin);
    password[strcspn(password, "\n")] = 0;
    
    tcsetattr(STDIN_FILENO, TCSANOW, &oldterm);
}

// Secure file handling
void secureConfigFile() {
    char config_path[MAX_LENGTH * 2];
    snprintf(config_path, sizeof(config_path), "%s/%s", getenv("HOME"), CONFIG_FILE);
    chmod(config_path, S_IRUSR | S_IWUSR);
}

void loadServers() {
    char config_path[MAX_LENGTH * 2];
    snprintf(config_path, sizeof(config_path), "%s/%s", getenv("HOME"), CONFIG_FILE);
    
    FILE *file = fopen(config_path, "r");
    if (!file) {
        printf(COLOR_YELLOW "Configuration file not found at %s. Creating new one.\n" COLOR_RESET, config_path);
        file = fopen(config_path, "w");
        if (!file) {
            printf(COLOR_RED "Error creating configuration file!\n" COLOR_RESET);
            exit(1);
        }
        fclose(file);
        secureConfigFile();
        return;
    }
    
    char line[MAX_LENGTH * 4];
    serverCount = 0;
    
    while (fgets(line, sizeof(line), file) && serverCount < MAX_ENTRIES) {
        if (line[0] == '#') continue; // Skip comments
        
        int result = sscanf(line, "%99[^|]|%99[^|]|%99[^|]|%99[^|]|%d|%d",
                           servers[serverCount].username,
                           servers[serverCount].ip,
                           servers[serverCount].description,
                           servers[serverCount].keyfile,
                           &servers[serverCount].port,
                           &servers[serverCount].use_password);
        
        if (result >= 4) { // At least username, ip, description, keyfile
            if (result < 5) servers[serverCount].port = 22; // Default SSH port
            if (result < 6) servers[serverCount].use_password = 0;
            serverCount++;
        }
    }
    
    fclose(file);
    secureConfigFile();
}

void saveServers() {
    FILE *file = fopen(CONFIG_FILE, "w");
    if (!file) {
        printf(COLOR_RED "Error saving configuration!\n" COLOR_RESET);
        return;
    }
    
    fprintf(file, "# SSH Manager Configuration\n");
    fprintf(file, "# Format: username|ip|description|keyfile|port|use_password\n");
    
    for (int i = 0; i < serverCount; i++) {
        fprintf(file, "%s|%s|%s|%s|%d|%d\n",
                servers[i].username,
                servers[i].ip,
                servers[i].description,
                servers[i].keyfile,
                servers[i].port,
                servers[i].use_password);
    }
    
    fclose(file);
    secureConfigFile();
    printf(COLOR_GREEN "Configuration saved successfully!\n" COLOR_RESET);
}

void displayMenu() {
    printf(COLOR_CYAN "\nSSH Connection Manager\n" COLOR_RESET);
    printf(COLOR_CYAN "======================\n" COLOR_RESET);
    printf(COLOR_BLUE "Available servers:\n\n" COLOR_RESET);
    
    for (int i = 0; i < serverCount; i++) {
        printf(COLOR_YELLOW "%d) %s@%s:%d\n" COLOR_RESET, 
               i+1, servers[i].username, servers[i].ip, servers[i].port);
        printf("   " COLOR_MAGENTA "Description: " COLOR_RESET "%s\n", servers[i].description);
        if (strlen(servers[i].keyfile) > 0) {
            printf("   " COLOR_GREEN "Using keyfile: " COLOR_RESET "%s\n", servers[i].keyfile);
        } else if (servers[i].use_password) {
            printf("   " COLOR_RED "Using password authentication\n" COLOR_RESET);
        }
        printf("\n");
    }
    
    printf(COLOR_YELLOW "%d) Add new server\n" COLOR_RESET, serverCount+1);
    printf(COLOR_YELLOW "%d) Delete server\n" COLOR_RESET, serverCount+2);
    printf(COLOR_YELLOW "%d) Exit\n" COLOR_RESET, serverCount+3);
    printf(COLOR_BLUE "\nSelect an option (1-%d): " COLOR_RESET, serverCount+3);
}

void connectSSH(int index) {
    if (index < 0 || index >= serverCount) {
        printf(COLOR_RED "Invalid selection!\n" COLOR_RESET);
        return;
    }
    
    printf(COLOR_GREEN "\nConnecting to %s@%s:%d...\n" COLOR_RESET, 
           servers[index].username, servers[index].ip, servers[index].port);
    
    char command[MAX_LENGTH * 5];
    if (strlen(servers[index].keyfile) > 0) {
        // Using SSH key
        snprintf(command, sizeof(command), 
                "ssh -i %s -p %d %s@%s",
                servers[index].keyfile,
                servers[index].port,
                servers[index].username,
                servers[index].ip);
    } else {
        // No authentication specified - will use SSH agent
        snprintf(command, sizeof(command),
                "ssh -p %d %s@%s",
                servers[index].port,
                servers[index].username,
                servers[index].ip);
    }
    
    system(command);
}

void addServer() {
    if (serverCount >= MAX_ENTRIES) {
        printf(COLOR_RED "Maximum number of servers reached!\n" COLOR_RESET);
        return;
    }
    
    SSHServer newServer;
    memset(&newServer, 0, sizeof(newServer));
    newServer.port = 22; // Default SSH port
    
    printf(COLOR_CYAN "\nAdd New Server\n" COLOR_RESET);
    printf("===============\n");
    
    printf("Username: ");
    scanf("%99s", newServer.username);
    while (getchar() != '\n'); // Clear buffer
    
    printf("IP/Hostname: ");
    scanf("%99s", newServer.ip);
    while (getchar() != '\n');
    
    printf("Description: ");
    fgets(newServer.description, sizeof(newServer.description), stdin);
    newServer.description[strcspn(newServer.description, "\n")] = 0;
    
    printf("Port (default 22): ");
    char port_str[10];
    fgets(port_str, sizeof(port_str), stdin);
    if (atoi(port_str) > 0) newServer.port = atoi(port_str);
    
    printf("Authentication method:\n");
    printf("1) SSH Key\n");
    printf("2) Password\n");
    printf("3) None (use default SSH agent)\n");
    printf("Choice (1-3): ");
    
    int auth_choice;
    scanf("%d", &auth_choice);
    while (getchar() != '\n');
    
    switch (auth_choice) {
        case 1:
            printf("Path to private key file: ");
            scanf("%99s", newServer.keyfile);
            while (getchar() != '\n');
            newServer.use_password = 0;
            break;
        case 2:
            newServer.use_password = 1;
            newServer.keyfile[0] = '\0';
            printf(COLOR_RED "Warning: Passwords will be stored in plain text in config file!\n" COLOR_RESET);
            break;
        default:
            newServer.use_password = 0;
            newServer.keyfile[0] = '\0';
            break;
    }
    
    servers[serverCount++] = newServer;
    saveServers();
}

void deleteServer() {
    if (serverCount == 0) {
        printf(COLOR_RED "No servers to delete!\n" COLOR_RESET);
        return;
    }
    
    printf(COLOR_RED "\nDelete Server\n" COLOR_RESET);
    printf("=============\n");
    printf("Enter server number to delete (1-%d): ", serverCount);
    
    int choice;
    scanf("%d", &choice);
    while (getchar() != '\n');
    
    if (choice < 1 || choice > serverCount) {
        printf(COLOR_RED "Invalid selection!\n" COLOR_RESET);
        return;
    }
    
    printf(COLOR_RED "Are you sure you want to delete %s@%s? (y/n): " COLOR_RESET,
           servers[choice-1].username, servers[choice-1].ip);
    char confirm;
    scanf("%c", &confirm);
    
    if (confirm == 'y' || confirm == 'Y') {
        // Shift all entries after the deleted one
        for (int i = choice-1; i < serverCount-1; i++) {
            servers[i] = servers[i+1];
        }
        serverCount--;
        saveServers();
        printf(COLOR_GREEN "Server deleted successfully!\n" COLOR_RESET);
    } else {
        printf(COLOR_YELLOW "Deletion cancelled.\n" COLOR_RESET);
    }
}

int main() {
    loadServers();
    
    while (1) {
        displayMenu();
        
        int choice;
        scanf("%d", &choice);
        while (getchar() != '\n'); // Clear buffer
        
        if (choice == serverCount + 1) {
            addServer();
        } else if (choice == serverCount + 2) {
            deleteServer();
        } else if (choice == serverCount + 3) {
            printf(COLOR_CYAN "Exiting...\n" COLOR_RESET);
            break;
        } else if (choice >= 1 && choice <= serverCount) {
            connectSSH(choice - 1);
        } else {
            printf(COLOR_RED "Invalid choice! Please try again.\n" COLOR_RESET);
        }
    }
    
    return 0;
}
