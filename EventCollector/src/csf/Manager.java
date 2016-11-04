package csf;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Scanner;

public class Manager {
	public static void main(String[] args) throws IOException{
		String command; //Comando a ser executado
		String specifier; //Especificador do comando (ex: data)
		Scanner sc = null; //Scanner para ler input
		//String path_file = args[0]; //path ou directoria onde o disco foi montado
		
		System.out.println("---------/|\\----------/|\\---------");
		System.out.println("---------\\|/ xTractor \\|/---------");
		System.out.println("Type HELP for a list of possible commands or EXIT to leave\n");
		
		//-------------------INICIO LOOP--------------------------------------------------------
		
		loop: while(true){							//loop para estar sempre a receber inputs
			System.out.print("xTractor /> ");
			sc = new Scanner(System.in);
			command = sc.next();					//ler primeira palavra do input
			specifier = null;
			
			switch (command){
				case "EVENT":							//COMANDO EVENTO-------------------------
					command = sc.next();
					
					if (command.equals("DATE")){
						specifier = sc.next();		//a *data* (formato: EVENT DATE *data*)
						//call eventlog function with 2 args (date, datespecifier)
					}
					else if (command.equals("WINDOWS")){
						//call eventlog function with 1 arg (windows)
					}
					else if (command.equals("APPSNSERVICES")){
						//call eventlog function with 1 arg (appnservc)
					}
					else 
						System.out.println("Wrong Command");
					
					break;
				case "REG":								//COMANDO REGISTRY------------------------
					command = sc.next();
				
					if (command.equals("NETWORK")){
						//call winregextractor function with 1 arg (network)
					}
					else if (command.equals("SYSTEM")){
					}
					else if (command.equals("TIMEZONE")){
					}
					else if (command.equals("SHARES")){
					}
					else if (command.equals("DEVICES")){	
					}
					else if (command.equals("USERS")){
					}
					else 
						System.out.println("Wrong Command");
					break;
				case "HELP":							//COMANDO HELP---------------------------
					try {
						BufferedReader br = new BufferedReader(new FileReader("ToolDescription.txt"));
						String line = null;
						   while ((line = br.readLine()) != null) {
						       System.out.println(line);
						   }
					} catch (FileNotFoundException e) {
						e.printStackTrace();
					}
					break;
				case "EXIT":							//COMANDO EXIT---------------------------
					break loop;
				default:								//BAD COMMAND----------------------------
					System.out.println("Wrong Command");
			}
		}
		sc.close();
		System.out.println("---xTraitor---");
	}
}
