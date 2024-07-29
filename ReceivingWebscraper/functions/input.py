from common import *
from functions.header import *

def is_H_number(s):
    # Define the regex pattern
    pattern = r'^H10306600\d{6}01049$'
    # Match the input string against the pattern
    return bool(re.match(pattern, s, re.IGNORECASE))

def six_to_H(s):
    return "H10306600" + s + "01049"


def read_input():
    while(True):
        user_input = input("Enter Waybill: ")
        if(len(user_input) == 6):
            return six_to_H(user_input)
        elif(is_H_number(user_input)):
            return user_input
        elif(user_input == "exit"):
            return "exit"
        print("No Valid Input, try again\n")


#This is a simple counter that tell how many packages have been done:
def update_counter(filename):
    try:
        with open(filename, 'r+') as file:
            # Read the current value
            current_value = int(file.read())
            # Increment the value
            new_value = current_value + 1
            # Move the cursor to the beginning of the file
            file.seek(0)
            print_value = new_value 
            print("PackageNumber: "+ str(print_value ))
            # Write the new value
            file.write(str(new_value))
            # Truncate the file to the current cursor position
            file.truncate()
    except FileNotFoundError:
        # If the file does not exist, create it and write '1'
        with open(filename, 'w') as file:
            file.write('1')