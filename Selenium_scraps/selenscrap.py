from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import csv


# To close the browesr back in the background we have options
options = ChromeOptions()
options.headless = True
driver_path = r"C:\Users\RISHABH AKAR\Desktop\Exchange\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(driver_path,options=options)
driver = webdriver.Chrome(service=service)
driver.get('https://directory.ntschools.net/#/schools')

selector= '#search-panel-container .nav-link'
links = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )
print(links)

# Implicit Selector
#driver.implicitly_wait(80)



# links = driver.find_elements(By.CSS_SELECTOR, selector)
links = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )
results = []
for i in range(5):
    

    links = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )
    # Attempt to click the link
    try:
        links[i].click()
    except Exception as e:
        print(f"Click failed: {e}. Retrying with ActionChains.")
        ActionChains(driver).move_to_element(links[i]).click().perform()
    # Wait for the school name element to be present
    school_name_selector = '.school-title h1'
    name_school = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, school_name_selector)))

    # Extract and print the text
    print(name_school.text)

     # Extract details
    details = {
        'name': name_school.text,
        'ph_address': WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//div[text()="Physical Address"]/following-sibling::div'))
        ).text,
        'po_address': WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//*[text()="Postal Address"]/following-sibling::*'))
        ).text,
        'phone': WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//*[text()="Phone"]/following-sibling::*/a'))
        ).text,
    }
    results.append(details)

    # Navigate back
    driver.back()

    # Re-fetch the links after navigating back
    links = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )

# Print the results
print(results)

# Close the driver
driver.quit()

# after driver exits()

with open('schools_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f,
                            fieldnames=['name', 'ph_address', 'po_address', 'phone'])
    writer.writeheader()
    writer.writerows(results)