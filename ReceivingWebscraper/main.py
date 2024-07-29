from common import *
from functions.header import *
from functions.login import *
from functions.input import *
from functions.huopin import *






def clear_and_verify_input(driver,input_element, max_attempts=3):
    attempt = 0
    if input_element.get_attribute('value') == '':
        return True
    while attempt < max_attempts:
        time.sleep(0.1)
        # Clear the input field using JavaScript
        driver.execute_script("arguments[0].value = '';", input_element)
        time.sleep(0.1)
        # Verify if the input field is cleared
        if input_element.get_attribute('value') == '':
            #print("Input element cleared successfully.")
            return True
        else:
            #print(f"Attempt {attempt + 1} failed to clear the input. Retrying...")
            attempt += 1
    
    print("Failed to clear the input element after multiple attempts.")
    return False

def save_input(waybill, filename):
    now = datetime.now()

    # Format the time as a string
    time_changed = now.strftime('%Y-%m-%d-%H-%M-%S')
    with open(filename, 'a', encoding='utf-8') as file:
            file.write(waybill + "; ")
            file.write(username + "; ")
            file.write(time_changed + "; ")
            file.write(canpin + "; ")
            file.write(zhengpin + "; ")
            file.write("\n")
            file.close()

def save_input_huopin(huopin_nr ,waybill, filename):
    now = datetime.now()

    # Format the time as a string
    time_changed = now.strftime('%Y-%m-%d-%H-%M-%S')
    with open(filename, 'a', encoding='utf-8') as file:
            file.write(waybill + "; ")
            file.write(username + "; ")
            file.write(time_changed + "; ")
            file.write(huopin_nr + "; ")
            file.write(canpin + "; ")
            file.write(zhengpin + "; ")
            file.write("\n")
            file.close()

def main():

    print("Version 0.0.1 \n")
    print("Alternative Return Interface for Cainiao Warehouse\n")
    
     # Whether to use headless or normal browser:
    options = Options()
    #options.headless = True

    if use_headless:
        options.add_argument("--headless=new")
        
        # Set up the WebDriver
    driver = webdriver.Chrome(options=options)
    #driver.implicitly_wait(20)
    # Basically Login with credentials:
    resolve_login_page(driver)
    print("Login Page resolved")

    body, input_element = resolve_landing_page(driver)

    while(True):        
        #current_value_length = len(input_element.get_attribute('value'))
        #if (current_value_length != 0):
        #    body, input_element = resolve_landing_page(driver,0.1)
        # JavaScript to select the content of the input element
        select_script = "arguments[0].select();"
        driver.execute_script(select_script, input_element)

        # Send the BACKSPACE key to clear the selected content
        input_element.send_keys(Keys.BACKSPACE)
        
        #driver.execute_script("arguments[0].value = '';", input_element)
        #input_element = driver.find_element(By.XPATH, "//input[@placeholder='扫描/输入运单号']")
        waybill_nr  = read_input()
        save_input(waybill_nr, "waybill.txt")
        if waybill_nr=="exit":
            driver.quit()
            return 0
        print(waybill_nr)
        #clear_and_verify_input(driver,input_element, 4)
        
        driver.execute_script("arguments[0].value = '';", input_element)
        time.sleep(0.1)
        #input_element = driver.find_element(By.XPATH, "//input[@placeholder='扫描/输入运单号']")
        #input_element.clear()
        #try:
        #    input_element.clear()
        #except:
        #    print("Can't clear field")
        input_element.send_keys(waybill_nr + Keys.ENTER)

        time.sleep(0.4)
        td_elements = driver.find_elements(By.XPATH, "//td[@data-next-table-col='0']")
        td_elements2 = driver.find_elements(By.XPATH, "//td[@data-next-table-col='1']")
        td_elements3 = driver.find_elements(By.XPATH, "//td[@data-next-table-col='2']")
        td_elements4 = driver.find_elements(By.XPATH, "//td[@data-next-table-col='3']")
        td_elements5 = driver.find_elements(By.XPATH, "//td[@data-next-table-col='4']")
        td_elements6 = driver.find_elements(By.XPATH, "//td[@data-next-table-col='5']")

        nr_huopin= len(td_elements)
        print("Items: " + str(nr_huopin))
        
        # Could implement function here that looks up package information if len = 0.
        # Check whether popup window is active. Click away if it is.
        if nr_huopin == 0:
            body.send_keys(Keys.ESCAPE)

        you_zheng = False
        you_can = False
        huopin_list = {}
        #content = {}
        #huopin_nr = {}
        #total_nr = {}
        #received_nr = {}
        #can_nr = {}
        #zheng_nr = {}
        for index, td_element in enumerate(td_elements):
            try: 
                huopin_list[index] = huopin(waybill_nr)
                huopin_list[index].huopin_nr = td_elements[index].text
                huopin_list[index].content = td_elements2[index].text
                huopin_list[index].total_nr = td_elements3[index].text
                huopin_list[index].received_nr = td_elements4[index].text
                huopin_list[index].can_nr = td_elements5[index].text
                huopin_list[index].zheng_nr = td_elements6[index].text
                save_input_huopin(td_elements[index].text ,waybill_nr, "Before.txt")
            except:
                print("Couldn't access index")

        driver.execute_script("arguments[0].value = '';", input_element)
        for index, td_element in enumerate(td_elements):
            youz, youc = resolve_huopin(huopin_list[index],driver, body)
            you_zheng = you_zheng or youz
            you_can = you_can or youc
            time.sleep(0.2)
            body.send_keys(Keys.ESCAPE)

        #current_value_length = len(input_element.get_attribute('value'))
        #for _ in range(current_value_length):
        #    input_element.send_keys(Keys.BACKSPACE)

        if (you_zheng and you_can):
            print(red + "Warning: Mixed Package, open!" + reset)
            # playsound('error.mp3')
            update_counter("counter.txt")
        if (you_zheng and not(you_can)):
            print(green + "Good Package, throw" + reset)
            #playsound('good.mp3')
            update_counter("counter.txt")
        if (not(you_zheng) and you_can):
            print(yellow + "Bad Package, throw" + reset)
            #playsound('bad.mp3')
            update_counter("counter.txt")
        if (not(you_zheng) and not(you_can)):
            print("Nothing booked")
        body = driver.find_element(By.XPATH, "//body")
        body.send_keys(Keys.ESCAPE)
    #driver.quit()
        



    return 0


if __name__ == "__main__":
    main()
