#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "winReg.c"

void greeting(){
    printf(" /****************************************\\\n");
    printf("|**************** xTractor ****************|\n");
    printf(" \\****************************************/\n");
    printf("\n");
}

void menu(){
    printf("Select from the menu:\n\n");
    printf("1 - System information\n");
    printf("2 - List all networks connected\n");
    printf("3 - List all devices plugged in\n");
    printf("4 - List recent files\n");
    printf("5 - List recent downloaded files\n");
    printf("6 - List recent launched programs\n");
    printf("7 - Physical location\n");
    printf("8 - Login history\n");
    printf("9 - Browser history\n");
    printf("0 - Help\n");
    printf("98 - About this tool\n");
    printf("99 - Exit\n\n");
}

void prompt(){
    printf(" > ");
}

int main(int argc, char *argv[])
{
    int command = 0;
    greeting();
    while(1){
        menu();
        prompt();
        scanf("%d", &command);
        switch(command){
            case 0 :
                printf("print help file\n");
                break;
            case 1 :
                extractOS("SYSTEM");
                break;
            case 2 :

                break;
            case 3 :

                break;
            case 4 :

                break;
            case 5 :

                break;
            case 6 :

                break;
            default:
                printf("Invalid choice\n");
        }
    }
    return 0;
}
