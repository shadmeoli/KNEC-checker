import time
import logging
import sqlite3
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import pyinputplus as pyip

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQLite connection and cursor
conn = sqlite3.connect('results.db')
cursor = conn.cursor()

def initialize_driver():
    # Specify the path to the chromedriver executable
    chrome_driver_binary = "/usr/bin/chromedriver"  # Adjust the path according

    # Create a Service object with the specified executable path
    service = Service(chrome_driver_binary)

    # Create ChromeOptions
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    # Instantiate the Chrome webdriver with the specified service and options
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def create_results_table():
    # Create a table to store the results
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            index_number TEXT,
            data TEXT
        )
    ''')
    conn.commit()

def insert_result(index_number, data_dict):
    # Serialize the dictionary to a JSON string before inserting into the database
    data_str = json.dumps(data_dict, indent=4)
    with open("results.json", "+w") as result_file:
        json.dump(data_dict)
        print("results added")

    # Insert the data into the results table
    cursor.execute('''
        INSERT INTO results (index_number, data)
        VALUES (?, ?)
    ''', (index_number, data_str))
    conn.commit()

def retrieve_results_from_db():
    # Retrieve and print data from the database
    cursor.execute("SELECT * FROM results")
    results = cursor.fetchall()
    for result in results:
        data_dict = json.loads(result[2])
        print(f"Index Number: {result[1]}, Data: {data_dict['data']}")

def get_user_input():
    # Use pyinputplus to ensure input is an int with a maximum of 3 digits
    min_index = pyip.inputInt(prompt="Enter lowest index: ", min=1)
    max_index = pyip.inputInt(prompt="Enter highest index: ", min=min_index)
    if max_index > min_index:
        return min_index, max_index
    else:
        logger.error("Max index must be greater than min index")
        raise ValueError("Max index must be greater than min index")

def clear_input_fields(driver, *elements):
    for element in elements:
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(element)).clear()
        except:
            pass

def main():
    # Replace with the actual URL of the webpage
    url = "https://results.knec.ac.ke"
    code = "08237001"  # Replace with the actual index number

    driver = initialize_driver()
    driver.get(url)

    index_field = (By.ID, "indexNumber")
    name_field = (By.ID, "name")
    search_button = (By.CSS_SELECTOR, "button.btn-primary")

    min_index, max_index = get_user_input()

    create_results_table()

    try:
        for index in range(min_index, max_index + 1):
            flag = False
            index_number = code + str(index).zfill(3)

            clear_input_fields(driver, index_field, name_field)

            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(index_field)).send_keys(index_number)

            for first_letter in range(65, 91):  # Loop through uppercase letters A-Z
                for second_letter in range(97, 123):  # Loop through lowercase letters a-z
                    if flag:
                        break
                    name = chr(first_letter) + chr(second_letter)

                    clear_input_fields(driver, name_field)

                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(name_field)).send_keys(name)
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(index_field)).send_keys(index_number)
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(search_button)).click()

                    try:
                        # Wait for data to appear in the target divs
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "row"))
                        )

                        # Extract and save the data
                        data_rows = driver.find_elements(By.CLASS_NAME, "row")[1:]
                        data = [row.text for row in data_rows]
                        if data != ['View Results\nPlease enter a valid index number and your registered name', 'View Results', '', '']:
                            # Modify the data format to be a dictionary
                            data_dict = {"data": data[2:]}
                            insert_result(index_number, data_dict)
                            logger.info(f"Data for index {index}: {data_dict}")
                            flag = True
                            WebDriverWait(driver, 10).until(EC.presence_of_element_located(name_field))
                            clear_input_fields(driver, name_field, index_field, search_button)
                            break

                        WebDriverWait(driver, 10).until(EC.presence_of_element_located(name_field))
                        clear_input_fields(driver, name_field, index_field, search_button)

                    except Exception as e:
                        logger.error(f"An error occurred: {e}")

    finally:
#        retrieve_results_from_db()
        driver.quit()
        conn.close()

if __name__ == "__main__":
    main()
