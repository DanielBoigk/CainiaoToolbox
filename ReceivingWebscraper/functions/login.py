from functions.header import *
from common import *

def resolve_login_page(driver):
    # write function get password:
    
    # Open the login page
    driver.get('https://owms-lite-de.cainiao.com/page/cainiao/cnwms/login')

    #Input Username
    username_input = driver.find_element(By.ID, 'username')
    username_input.clear()
    username_input.send_keys(username)
    time.sleep(0.2)
    #Input Password
    password_input = driver.find_element(By.ID, 'bw')  
    password_input.clear()
    password_input.send_keys(password)
    time.sleep(0.2)
    # Resolve checkbox
    checkbox = driver.find_element(By.ID, 'agree') 
    checkbox.click()
    time.sleep(0.2)
    #Press Login button:
    buttons = driver.find_elements(By.XPATH, "//button")
    buttons[0].click()
    return

def resolve_landing_page(driver, time_sleep = 2):
    time.sleep(time_sleep)
    # Open return page:
    driver.get("https://owms-lite-de.cainiao.com/page/inbound/receive/cnlReturnReceive?")
    print("\nReturn Interface Ready\n")

    body = driver.find_element(By.XPATH, "//body")
    # Reason #1 for crash cannot find this field, crashes, because website loads too slow...
    #input_element = driver.find_element(By.XPATH, "//input[@placeholder='扫描/输入运单号']")
    wait = WebDriverWait(driver, 10)
    try: 
        input_element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='扫描/输入运单号']")))
    except:
        print("ReturnPage Loads a little bit longer: Retrying:")
        for i in range(5):
            try:
                input_element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='扫描/输入运单号']")))
                break
            except:
                print("ReturnPage Loads a little bit longer: Retrying:")
    return body, input_element