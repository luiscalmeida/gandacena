#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//#include "winReg.c"

#define KNRM  "\x1B[0m"
#define KRED  "\x1B[31m"
#define KGRN  "\x1B[32m"
#define KYEL  "\x1B[33m"
#define KBLU  "\x1B[34m"
#define KMAG  "\x1B[35m"
#define KCYN  "\x1B[36m"
#define KWHT  "\x1B[37m"

void greeting(){
    printf("\n");
    printf("\t %s/****************************************\\\n", KRED);
    printf("\t|**************** xTractor ****************|\n");
    printf("\t \\****************************************/\n");
    printf("\n");
}

void menu(){
    printf("\t\t%s    Select from the menu:\n\n", KRED);
    printf("\t\t1 - System information\n");
    printf("\t\t2 - List all networks connected\n");
    printf("\t\t3 - List all devices plugged in\n");
    printf("\t\t4 - List recent files\n");
    printf("\t\t5 - List recent downloaded files\n");
    printf("\t\t6 - List recent launched programs\n");
    printf("\t\t7 - Physical location\n");
    printf("\t\t8 - Login history\n");
    printf("\t\t9 - Browser history\n");
    printf("\t\t0 - Help\n");
    printf("\t\t98 - About this tool\n");
    printf("\t\t99 - Exit\n");
    printf("\n");
}

void help(){
    printf("\t%sHelp menu:\n\n", KWHT);
    printf("1 - Operating system's information as it's version, architecture, etc..\n");
    printf("2 - ESSID(name), IP and date of connections to any AP's stored in the system.\n");
    printf("3 - Names and dates of connections of USB, external storage devices, input and output devices to the system.\n");
    printf("4 - Recently opened or modified files of any extension.\n");
    printf("5 - Recently downloaded files from Chrome, Firefox or InternetExplorer.\n");
    printf("6 - Recently executable programs executed on the system.\n");
    printf("7 - Information about the possible physical location where this system may have been used most of the time.\n");
    printf("8 - Names of recently logged in or logged out users on the system.\n");
    printf("9 - Recently searched URL's on Chrome, Firefox or InternetExplorer.\n");
    printf("0 - Will display this menu.\n");
    printf("98 - Will display info about the tool and team that implemented it.\n");
    printf("99 - Will exit the tool.\n");
    printf("\n");
}

void about(){
    printf("%sxTractor is a post-mortem forensic tool designed to run on linux operating systems.\n", KWHT);
    printf("It will expect a file system image (dd image) as input and will extract certain data from the file system's windows registry and other sources.\n");
    printf("It was develop by a team of three young IT engineers as a subject of Ciber Security Forensic course.\n");
    printf("2016 Instituto Superior Tecnico\n");
    printf("\n");
}

void prompt(){
    printf("%s > ", KWHT);
}

int main(int argc, char *argv[])
{
    system("setterm -bold on");
    int command;
    char *ptr, buffer[20];	
    greeting();
    while(1){
        menu();
        prompt();
	scanf(" %s", &buffer);
	printf("%s\n", KWHT);
	command = strtol(buffer, &ptr, 10);
	if(buffer == ptr){
		command = 100;
	}
        switch(command){
            case 0: 
                help();
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
	    case 98 : 
		about();
                break;
	    case 99 :
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
