# change when using:
use_headless = False
username = '' # 25=Yezi; 10= Daniel 
password = ''


canpin = ""

zhengpin = ""

cp_GZ = "cp01-CP01-GZ-7"
zp_GZ = "zp01-GAOZ-7"
cp_LEER = "cp01-LEER-02"
zp_LEER = "zp01-LEER-02"

is_GZ = False

def process_line(line):
    # Split the line at the '#' character
    parts = line.split('#')
    # Strip trailing spaces or tabs from the first part
    processed_part = parts[0].rstrip(' \t')
    # Reconstruct the string with the comment part
    return processed_part



def read_login_data():
    global username, password, canpin, zhengpin, cp_GZ, zp_GZ, cp_LEER, is_GZ, use_headless
    with open("common.txt", "r") as file:
        lines = file.readlines()
        username = process_line(lines[0].strip())
        password = process_line(lines[1].strip())
        canpin = process_line(lines[2].strip())
        zhengpin = process_line(lines[3].strip())
        cp_GZ = process_line(lines[4].strip())
        zp_GZ = process_line(lines[5].strip())
        cp_LEER = process_line(lines[6].strip())
        is_GZ = ("True" == process_line(lines[7].strip()))
        use_headless = ("True" == process_line(lines[8].strip()))
    return True

read_login_data()