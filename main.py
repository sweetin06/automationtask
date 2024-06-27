import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument("start-maximized")
# options.headless = True

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def login():
    driver.get("https://demo.openmrs.org/openmrs/login.htm")  # Replace with your URL

    user_name = driver.find_element(By.ID, "username")
    user_name.send_keys("Admin")

    password = driver.find_element(By.ID, "password")
    password.send_keys("Admin123")

    ul_element = driver.find_element(By.ID, "sessionLocation")
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")
    select_location = li_elements[2]
    select_location.click()

    submit_btn = driver.find_element(By.ID, "loginButton")
    submit_btn.click()

    current_url = driver.current_url
    if current_url == "https://demo.openmrs.org/openmrs/referenceapplication/home.page":
        print("Login successful")
    else:
        print("Login failed, verify the code")


def click_next_button():
    next_btn = driver.find_element(By.ID, "next-button")
    next_btn.click()


def patient_registration():
    expected_data = {
        "givenName": "sweetin",
        "familyName": "aalesta",
        "gender": "Female",
        "birthdateDay": "06",
        "birthdateMonth": "5",
        "birthdateYear": "2000",
        "address1": "kanyakumari",
        "phoneNumber": "9787878787"
    }

    try:
        buttons = driver.find_elements(By.XPATH, "//a[@type='button']")
        for reg_button in buttons:
            if "Register a patient" in reg_button.text:
                reg_button.click()
                break

        # Fill in the form fields
        driver.find_element(By.NAME, "givenName").send_keys(expected_data["givenName"])
        driver.find_element(By.NAME, "familyName").send_keys(expected_data["familyName"])
        click_next_button()

        gender_select = Select(driver.find_element(By.ID, "gender-field"))
        gender_select.select_by_value("F")
        click_next_button()

        driver.find_element(By.NAME, "birthdateDay").send_keys(expected_data["birthdateDay"])
        birth_month = Select(driver.find_element(By.NAME, "birthdateMonth"))
        birth_month.select_by_value(expected_data["birthdateMonth"])
        driver.find_element(By.NAME, "birthdateYear").send_keys(expected_data["birthdateYear"])
        click_next_button()

        driver.find_element(By.ID, "address1").send_keys(expected_data["address1"])
        click_next_button()

        driver.find_element(By.NAME, "phoneNumber").send_keys(expected_data["phoneNumber"])
        click_next_button()
        click_next_button()  # Proceed to the confirmation page

        # Wait for the confirmation page to load
        time.sleep(2)

        # Verify the displayed values on the confirmation page
        verify_values(expected_data)

    finally:
        print("FINISH")
        driver.quit()


def verify_values(expected_data):
    try:
        # Get the displayed values from the confirmation page
        displayed_values = {}
        p_elements = driver.find_elements(By.XPATH, '//div[@id="dataCanvas"]/div/p')

        for p in p_elements:
            title = p.find_element(By.XPATH, './span[@class="title"]').text.strip()
            value = p.text.replace(title, '').strip()
            displayed_values[title] = value

        # Assert that the displayed values match the expected data using 'in' keyword
        assert expected_data["givenName"] in displayed_values[
            "Name:"], f"Expected Name: {expected_data['givenName']} in {displayed_values['Name:']}"
        assert expected_data["familyName"] in displayed_values[
            "Name:"], f"Expected Family Name: {expected_data['familyName']} in {displayed_values['Name:']}"
        assert expected_data["gender"] in displayed_values["Gender:"]

        # Convert birthdate month to full name using datetime
        birthdate_month_name = datetime.strptime(expected_data["birthdateMonth"], "%m").strftime("%B")
        expected_birthdate = f"{expected_data['birthdateDay']}, {birthdate_month_name}, {expected_data['birthdateYear']}"

        assert expected_birthdate in displayed_values["Birthdate:"]
        assert expected_data["address1"] in displayed_values["Address:"]
        assert expected_data["phoneNumber"] in displayed_values["Phone Number:"]

        print("Verification successful! All values match.")

    except AssertionError as e:
        print(f"Verification failed: {str(e)}")
        raise  # Re-raise the AssertionError to fail the test

    except Exception as e:
        print(f"An error occurred during verification: {str(e)}")
        raise  # Re-raise the exception to fail the test


"""def confirm_btn():
    confirm_btn = driver.find_element(By.ID,"submit")
    confirm_btn.click()"""


# Perform the login and patient registration process
login()
patient_registration()
#confirm_btn()


driver.close()

