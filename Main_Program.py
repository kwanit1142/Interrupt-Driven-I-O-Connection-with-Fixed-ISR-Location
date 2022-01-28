import os
import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
from os import system, name
from time import sleep

# By-Default, the state and program counter of microprocessor are taken as 0 and 100 respectively.
# For Device-config, the history for microprocessor actions is tapped as well.
# For Each and Every Operation, the respective locations and contribution to Program Counter were assigned as well.

microprocessor_state = 0                                           # default microprocessor state settings
microprocessor_pc = 100                                            # default program counter settings
microprocessor_history = [[microprocessor_state,microprocessor_pc]]
output_register = '0x8006'                                         # register location for output peripheral
data_operations_pc = [5,10,15,20]                                  # locations associated with data-import peripheral operations
keyboard_operations_pc = [25,30,35,40,45,50]                       # locations associated with keyboard peripheral operations
action=0                                                           # default value for action choice
run = "y"                                                          # enabling the model

# Function to Clear the Screen with each iteration

def screen_clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

# Function to keep track of changes in Microprocessor state, program counter and history

def history_compile(state=None,pc=None,history=None):
  history.append([state,pc])                                        # nested list storage for state and program counter changes
  return history

# Function to implement keyboard-based communication with Microprocessor and Output Peripheral

def keyboard_operations(mic_history=microprocessor_history,pc=keyboard_operations_pc,action=None,input_display=None,input_num1=None,input_num2=None):
  history_update=history_compile(1,pc[action],mic_history)
  sleep(1)                                                          # mimicing the interrupt as a single-second interval
  print(" ")
  print("Feeding the Input to Program Memory")
  print(" ")
  sleep(1)                                                          # mimicing the interrupt as a single-second interval
  print("Current State of Microprocessor = ",1)
  print("Current Program Counter = ",pc[action])
  print("Current Microprocessor History = ",history_update)
  print(" ")
  sleep(1)                                                          # mimicing the interrupt as a single-second interval
  print("Fetching the Output from Program Memory\n")
  sleep(1)                                                          # mimicing the interrupt as a single-second interval
  if action==0:
    print(input_display)
    history_update=history_compile(0,history_update[-2][-1],history_update)
  elif action==1:
    output = input_num1 + input_num2
    print(output)
    history_update=history_compile(0,history_update[-2][-1],history_update)
  elif action==2:
    output = input_num1 - input_num2
    print(output)
    history_update=history_compile(0,history_update[-2][-1],history_update)
  elif action==3:
    output = input_num1 * input_num2
    print(output)
    history_update=history_compile(0,history_update[-2][-1],history_update)
  elif action==4:
    output = input_num1 / input_num2
    print(output)
    history_update=history_compile(0,history_update[-2][-1],history_update)
  else:
    output = input_num1 % input_num2
    print(output)
    history_update=history_compile(0,history_update[-2][-1],history_update)
  return history_update

# Function to implement datafile-based communication with Microprocessor and Output Peripheral

def data_operations(mic_history=microprocessor_history,pc=data_operations_pc,action=None,input_path=None):
  history_update=history_compile(2,pc[action],mic_history)
  sleep(1)                                                          # mimicing the interrupt as a single-second interval
  print(" ")
  print("Feeding the Input to Program Memory")
  print(" ")
  print("Current State of Microprocessor = ",2)
  print("Current Program Counter = ",pc[action])
  print(" ")
  sleep(1)                                                          # mimicing the interrupt as a single-second interval
  print("Fetching the Output from Program Memory\n")
  sleep(1)                                                          # mimicing the interrupt as a single-second interval
  if action==0:
    output = open(input_path,"r")
    print(output.read())
    history_update=history_compile(0,history_update[-2][-1],history_update)
  elif action==1:
    output = pd.read_csv(input_path)
    print(output)
    history_update=history_compile(0,history_update[-2][-1],history_update)
  elif action==2:
    output = pd.read_excel(input_path)
    print(output)
    history_update=history_compile(0,history_update[-2][-1],history_update)
  else:
    output = np.load(input_path)
    print(output)
    history_update=history_compile(0,history_update[-2][-1],history_update)
  return history_update

# Function to assign input peripheral register in device config

def device_config():
  input_peripheral = int(input("Enter the choice of Input Peripheral:- 0 for Keyboard and 1 for Data Importing Device==> "))
  if input_peripheral==0:
    input_register='0x8000'                                         # Register for Input Peripheral as Keyboard
  elif input_peripheral==1:
    input_register='0x8001'                                         # Register for Input Peripheral as Data-Importing Device
  else:
    print("Invalid Entry according to System's Capability")
    input_register=input_default_register                           # Register for Input Peripheral as Default Configuration
  return input_register,input_peripheral

# Function to print the overall history of changes in microprocessor

def device_config_history(state,pc,history):
  print(" ")
  print("Current State of Microprocessor = ",state)
  print("Current Program Counter = ",pc)
  print("Microprocessor History = ",history)
  print(" ")

# Model for I/O Communication with Interrupt and Fixed ISR Locations

def fixed_ISR_model(state=None,pc=None,history=None,output_register=None):
  print(" ")
  print("Welcome to Interrupt-driven I/O Connection Modelling with fixed ISR Location")
  print(" ")
  input_register,input_choice = device_config()
  if input_choice==0 or input_choice==1:
    print(" ")
    print("Register corresponding to Input Peripheral ==> ",input_register)
    print("Register corresponding to Output Peripheral ==> ",output_register)
    print("Current State of Microprocessor = ",state)
    print("Current Program Counter = ",pc)
    print(" ")
    if input_choice==0:
      user_action = int(input("Enter the choice of action\n 0 for display\n 1 for adding 2 numbers\n 2 for subtracting 2 numbers\n 3 for multiplying 2 numbers\n 4 for dividing 2 numbers\n 5 for modulus between 2 numbers\n\n Choice_Input ==> "))
      if user_action==0:
        print(" ")
        user_input = input("Enter the Input ==> ")
        print(" ")
        history = keyboard_operations(mic_history = history,action=user_action,input_display=user_input)
      elif user_action==1 or user_action==2 or user_action==3 or user_action==4 or user_action==5:
        print(" ")
        user_num1 = int(input("Enter 1st Number ==> "))
        user_num2 = int(input("Enter 2nd Number ==> "))
        print(" ")
        history = keyboard_operations(mic_history = history,action=user_action,input_num1=user_num1,input_num2=user_num2)
      else:
        print(" ")
        print("Invalid Entry according to System's Capability")
        print(" ")
    else:
      user_action = int(input("Enter the choice of action\n 0 for text file\n 1 for csv file\n 2 for xlsx file\n 3 for numpy file\n\n Choice_Input ==> "))
      if user_action==0 or user_action==1 or user_action==2 or user_action==3:
        print(" ")
        user_path=input("Enter the File Path along the file name ==> ")
        print(" ")
        history = data_operations(mic_history = history,action=user_action,input_path=user_path)
      else:
        print(" ")
        print("Invalid Entry according to System's Capability")
        print(" ")
  return state,pc,history

# Main Function and Program

screen_clear()
while run=="y":
  microprocessor_state,microprocessor_pc,microprocessor_history = fixed_ISR_model(microprocessor_state,microprocessor_pc,microprocessor_history,output_register)
  microprocessor_pc+=1                                         # Program Counter incremented by single unit
  microprocessor_history[-1][-1] = microprocessor_pc           # In Microprocessor History, the latest Program Counter incremented by single unit
  print(" ")
  run = input("Continue[y/n] ==> ")                            # System Prompt asking to continue looping the I/O Communication model again
  screen_clear()
device_config_history(microprocessor_state,microprocessor_pc,microprocessor_history)