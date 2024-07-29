# Necessary imports:
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from datetime import datetime
#from playsound import playsound
import re


# Define Colors:

green = '\033[92m'
#yellow = '\033[93m'
red = '\033[91m'

yellow = '\033[35m'
reset = '\033[0m'  # Reset to default color
