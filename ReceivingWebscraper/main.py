

# If you want me to bugfix and extend this tool write me a mail via dn.boigk@gmail.com
# It is still very provisoric and I did not have the time to test it properly or include the features I had in mind.
# (Like Search function, check if Package is booked properly, ...) Since people only cared about nr. of packages... Not Lines of Code
# In case someone aquires an API key for Cainiao Warehouse it would be way easier.
# This Website gives an Overview on the Cainiao API: https://open.cainiao.com/api-doc/overview
# Possibly one could even avoid the too many clicks the quality control has to do on the handheld device
# The website from Cainiao has been written by idiots and is wasting everyones lifetime.




from functions.common import *
from functions.header import *
from functions.login import *
from functions.input import *
from functions.huopin import *
from functions.packages import *


def main():
    #input_queue = queue.Queue()
    #package_thread = threading.Thread(target=do_packages)
    do_packages()
    while(True):
        time.sleep(100)
    return 0

if __name__ == "__main__":
    main()
