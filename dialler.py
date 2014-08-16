# ----- INIT ROUTINE ----- #
import serial	#Import serial module from library
import time 	#Import time module from library (for 5s countdown)
import os
import sys 
import ConfigParser


# ----- SETUP CONFIG OPTIONS ----- #
conf = ConfigParser.ConfigParser()

def findConfigOption(section):
    dict1 = {}
    options = conf.options(section)
    for option in options:
        try:
            dict1[option] = conf.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
	
	
if os.path.exists("dialler.ini") == False:
	print "Writing new config."
	tonetime = 10
	waittime = 3.5
	
	port = "COM1"
	speed = 300

	logfile = "call_log.csv"

	configfile = open("dialler.ini","w")

	
	conf.add_section('Dialling')
	conf.add_section('Hardware')
	conf.add_section('Software')
	conf.set('Dialling','tonetime',tonetime)
	conf.set('Dialling','WaitTime',waittime)
	conf.set('Hardware','port',port)
	conf.set('Hardware','speed',speed)
	conf.set('Software','logfile',logfile)
	
	conf.write(configfile)
	configfile.close()
	
conf.read("dialler.ini")


# ----- END OF CONFIG SETUP -----#


os.system('cls' if os.name == 'nt' else 'clear')
modem = serial.Serial(findConfigOption('Hardware')['port'],findConfigOption('Hardware')['speed']) #Open COM port for serial communications and call it "modem"
modem.write("ATS11=" + str(findConfigOption("Dialling")['tonetime']) + "\r")
print "Serial port in use: " + modem.name	#Print which serial port is actually in use
time.sleep(1)
# ----- END INIT ROUTINE ----- #




def convert(num):
	newNumber = ''
	validNums = "123456789"
	for char in num:
		if char in validNums:
			newNumber = newNumber + str(char)
		if char == "0":
			newNumber = newNumber + str(char)
	return newNumber
	
def dial(number):
	print "Dialling " + number + "..."
	modem.write("ATDT " + number + "\r")	#Hopefully write the dial command and number to the modem and send a CR.
	time.sleep(float(findConfigOption("Dialling")['waittime']))	#Wait here for 5 seconds to give the modem time to dial out
	raw_input("Pick up the handset and press Enter")
	modem.write("\r")	#Send a CR to hang up the modem
	return
	
def writeOut(number):
	logFile = open(str(findConfigOption("Software")["logfile"]),"a")	#Open (and create) log file
	logFile.write('"' + number + '"' + "," + '"' + time.strftime("%H:%M") + '"' + "," + '"' + time.strftime("%d/%m/%Y") + '"' + "\n") 	#Write number + time + date to file
	logFile.close()
	return
	
# ------ MAIN PROGRAM ----- #	

if len(sys.argv) == 2:
	num = str(sys.argv[1])
	newNumber = convert(num)
	print newNumber
	dial(newNumber)
	writeOut(newNumber)
	os.system('cls' if os.name == 'nt' else 'clear')
else:
	while True:
		num = str(raw_input("Please enter the number you wish to dial, or type exit to quit: ")) #Remind yourself that you have to dial
		if num.lower() == "exit":
			print "Quitting...."
			exit()
		newNumber = convert(num)
		dial(newNumber)
		writeOut(newNumber)
		os.system('cls' if os.name == 'nt' else 'clear')

