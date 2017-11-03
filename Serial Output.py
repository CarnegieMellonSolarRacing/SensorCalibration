##########################################
# Arduino Voltage Reader
# Joel Anyanti
#10/26/2017
##########################################

##########################################
# Imports
##########################################
import csv
import serial
import time
import matplotlib.pyplot as plt #import matplotlib library
from drawnow import *
import keyboard

##########################################
# Graph Function
##########################################

def graphOutput(): #Create a function that makes our desired plot
    plt.ylim(0,3)                         #Set y min and max values based on known voltage quantity
    plt.title('Volatge Level Reader')
    plt.grid(True)
    plt.ylabel('Voltage')
    plt.plot(voltage, '-', label='Volts')
    plt.legend(loc='upper left')
    plt.xlabel("Time(s)")
    plt2 = plt.twinx()
    plt.ylim(0,0.05)                     # Set y min and max values based on expected current
    plt2.plot(amperage, "r-", label="Amps")
    plt2.ticklabel_format(useOffset=False)
    plt2.set_ylabel("Amperage(mA)")
    plt2.legend(loc="upper right")

##########################################
# Main Function
##########################################

# define global variables
voltage_reader = serial.Serial('COM4', baudrate=9600, timeout=1) # check Arduino IDE for Port Number
voltage = []
amperage = []
resistance = float(input("What is the Resistance of Load    ")) # used to approximate current draw
csv_file = open("voltage.csv", "w", newline="")
writer = csv.writer(csv_file, dialect="excel",) # define parameters for excel output
plt.ion()


startTime = time.time()
# voltage output loop
while True:
    if keyboard.is_pressed('ctrl+c'): # break cycle on key press command
        plt.savefig('voltage.pdf')
        plt.close()
        break
    drawnow(graphOutput)
    plt.pause(0.0001)
    volt_reading = float(voltage_reader.read(6).strip())
    writer.writerow([volt_reading])
    voltage.append(volt_reading)
    amperage.append(volt_reading/resistance)

# Find total time
endTime = time.time()
duration = endTime - startTime
sum = sum(amperage)
print(duration)




