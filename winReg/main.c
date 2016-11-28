#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//#include "winReg.c"

void greeting(){
    printf("\t /****************************************\\\n");
    printf("\t|**************** xTractor ****************|\n");
    printf("\t \\****************************************/\n");
    printf("\n");
}

void menu(){
    printf("\t\tSelect from the menu:\n\n");
    printf("\t1 - System information\n");
    printf("\t2 - List all networks connected\n");
    printf("\t3 - List all devices plugged in\n");
    printf("\t4 - List recent files\n");
    printf("\t5 - List recent downloaded files\n");
    printf("\t6 - List recent launched programs\n");
    printf("\t7 - Physical location\n");
    printf("\t8 - Login history\n");
    printf("\t9 - Browser history\n");
    printf("\t0 - Help\n");
    printf("\t98 - About this tool\n");
    printf("\t99 - Exit\n\n");
}

void prompt(){
    printf(" > ");
}


int clean_stdin()
{
    while (getchar()!='\n');
    return 1;
}

int main(int argc, char *argv[])
{
    int command = 0;
	char c; 	
    greeting();
    while(1){
        menu();
        prompt();
        while((scanf(" %d%c", &command, &c)!=2 || c!='\n') && clean_stdin()){} 
	//while ((c = getchar()) != '\n' && c != EOF) { } //DO NOT take this line
	printf("\n");
        switch(command){
            case 0:
                printf("print help file\n");
                break;
            case 1 :
                //extractOS("SYSTEM");
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
	    case 7 :
                break;
	    case 8 :	
                break;
	    case 9 :
                break;
	    case 97 :
		break;
	    case 98:
		printf("xTractor is a post-mortem forensic tool that will extract certain data from windows registry of a ntfs file system image given as imput. It was develop by a team of three young IT engineers as a subject of Ciber Security Forensic course.\n");
                break;
	    case 99:
		printf("Thank you for using xTractor!\n");
		exit(0);
                break;
            default:
                printf("Invalid choice\n");
		break;
        }
	printf("\n");
    }
    return 0;
}
