from common import *
from functions.header import *

class huopin:
    yundan_nr = ""
    huopin_nr = ""
    content = ""
    total_nr = ""
    received_nr = ""
    can_nr = ""
    zheng_nr = ""
    time_changed = ""
    storage_location = ""
    username = ""

    def __init__(self, yundan_nr):
        self.yundan_nr = yundan_nr
    def to_file(self, filename):
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(self.yundan_nr + "; ")
            file.write(self.huopin_nr + "; ")
            file.write(self.content + "; ")
            file.write(self.total_nr + "; ")
            file.write(self.received_nr + "; ")
            file.write(self.can_nr + "; ")
            file.write(self.zheng_nr + "; ")
            file.write(self.time_changed + "; ")
            file.write(self.storage_location + "; ")
            file.write(self.username + "; ")
            file.write("\n")
            file.close()
    

class element_attribute_contains_substring(object):
    def __init__(self, locator, attribute, substring):
        self.locator = locator
        self.attribute = attribute
        self.substring = substring

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        attribute_value = element.get_attribute(self.attribute)
        print(attribute_value)
        return self.substring in attribute_value




def resolve_huopin(huopin_var, driver, body):
    output = ""
    yc = False
    yz = False

    output += huopin_var.huopin_nr + "\n"
    output += huopin_var.content + "\n"
    try:
        wait = WebDriverWait(driver, 20)  # Wait up to 20 seconds
    # Wait until the input element with the placeholder '扫描/输入货品条码' is present
        huopin_element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='扫描/输入货品条码']")))
    except:
        print("webpage didn't load element for ")
        return False, False
    huopin_element.clear()
    select_script = "arguments[0].select();"
    driver.execute_script(select_script, huopin_element)

        # Send the BACKSPACE key to clear the selected content
    huopin_element.send_keys(Keys.BACKSPACE)
    huopin_element.send_keys(huopin_var.huopin_nr + Keys.ENTER)
    #time.sleep(0.3)
    if huopin_var.total_nr == huopin_var.received_nr: 
        if (huopin_var.can_nr != "0"):
            color = yellow
            output += "Bad Package"
        else:
            color = green
            output += "Good Package"
        print(color + output + reset)
        return False, False #, output

    try:
        wait = WebDriverWait(driver,20)
        checkbox = wait.until(EC.presence_of_element_located((By.ID, 'normal')))
        checkbox = driver.find_element(By.ID, 'normal')  # Using the ID attribute
    except:
        print("Can't find Checkbox. Is there an element opened?")
        return False, False #, output
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable(checkbox))
    # Retrieve the value of the aria-checked attribute
    aria_checked = checkbox.get_attribute('aria-checked')
    location = ""
    if aria_checked == "false":
        color = yellow
        output += "Bad Package\n"
        print(color + output + reset)
        huopin_var.storage_location = canpin
        #time.sleep(0.5)
        #canzheng_element = driver.find_element(By.ID, 'cabinetId') 
        try:
            wait = WebDriverWait(driver, 20)  # Wait up to 20 seconds
            # Wait until the canzheng_element with the ID 'cabinetId' is present
            canzheng_element = wait.until(EC.presence_of_element_located((By.ID, 'cabinetId')))
            shuliang_element = wait.until(EC.presence_of_element_located((By.ID, 'quantity')))
        except:
            print("cannot locate input")
            return False, False
        #time.sleep(0.5)
        location = canpin
        yc = True
    else:
        output += "Good Package\n"
        color = green
        print(color + output + reset)
        huopin_var.storage_location = zhengpin
        #time.sleep(0.5)
        #canzheng_element = driver.find_element(By.ID, 'cabinetId') 
        try:
            wait = WebDriverWait(driver, 20)  # Wait up to 20 seconds
            # Wait until the canzheng_element with the ID 'cabinetId' is present
            canzheng_element = wait.until(EC.presence_of_element_located((By.ID, 'cabinetId')))
            shuliang_element = wait.until(EC.presence_of_element_located((By.ID, 'quantity')))
        except:
            print("cannot locate input")
            return False, False
        #time.sleep(0.2)
        location = zhengpin
        yz = True
    #select_script = "arguments[0].select();"
    #driver.execute_script(select_script, canzheng_element)
    # Send the BACKSPACE key to clear the selected content
    #canzheng_element.send_keys(Keys.BACKSPACE)
    #canzheng_element.clear()
    
    canzheng_element.send_keys(location)
    #aria_valuetext1 = canzheng_element.get_attribute("aria-valuetext")
    F2_button = driver.find_element(By.CLASS_NAME, "next-btn.next-medium.next-btn-normal")
    #F2_button.click()
    #WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value(canzheng_element.text,location))
    #side_body= wait.until(EC.presence_of_element_located((By.ID, 'rehtml-lz716ye1')))
    #time.sleep(0.2)
    """
    try:
        WebDriverWait(driver, 10).until(element_attribute_contains_substring(canzheng_element, "aria-valuetext", location))
    except:
        print("Cannot write location into Field")
    aria_valuetext = canzheng_element.get_attribute("aria-valuetext")
    print(aria_valuetext)
    """

    time.sleep(0.3)
    shuliang_element.send_keys(huopin_var.total_nr)
    time.sleep(0.4)    
    body.send_keys(Keys.F2)

    # Get the current time
    now = datetime.now()

    # Format the time as a string
    huopin_var.time_changed = now.strftime('%Y-%m-%d-%H-%M-%S')
    huopin_var.username = username
    huopin_var.to_file("Orders.txt")
    #time.sleep(0.5)
    element_text = ""
    wait = WebDriverWait(driver, 20)  # Wait for up to 10 seconds
    try:
        F8_Button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='next-btn next-medium next-btn-primary' and @type='button']")))
    except:
        print("Cannot resolve F8 Button in time")
        return False, False
    table_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@data-next-table-row='0']")))
    for i in range(len(table_elements)):
        element_text += table_elements[i].text
    """
    try: 
        wait = WebDriverWait(driver, 10)  # Wait for up to 10 seconds
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//td[@class='next-table-cell' and @data-next-table-col='2' and @data-next-table-row='0' and @role='gridcell']")))
    # Read the text of the element
        
    except:
        print("Couldn't confirm Booking: Location not confirmed.")
        body.send_keys(Keys.F4)
        return False, False
    element_text = element.text
    print(element_text)
    """
    if ((location not in element_text) or (location =="")):
        body.send_keys(Keys.F4)
        shuliang_element.send_keys(huopin_var.total_nr)
        time.sleep(0.2)
        body.send_keys(Keys.F2)
        
    # Get the text content of the html element
    
    if ((location not in element_text) or (location =="")):
        body.send_keys(Keys.F4)
        return False, False
    """
    html_text = html_element.text
    checked = False
    if aria_checked ==False:
        c_count = html_text.count(canpin)
        print(c_count)
        if (c_count ==2):
            checked = True
    else:
        z_count = html_text.count(zhengpin)
        if (z_count ==2):
            checked = True
    """
    """
    if checked:
        body.send_keys(Keys.F8)
        return yz, yc #, output
    else:
        body.send_keys(Keys.F4)
        return False, False #, output
    """    
    
    body.send_keys(Keys.F8)
    #print("Target reached")
    return yz, yc #, output
    
