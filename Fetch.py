from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, TimeoutException
import time
# Initialize the browser driver
driver = webdriver.Chrome()  # Make sure to have the chromedriver in your PATH
driver.get("http://sdetchallenge.fetch.com")  # Replace with the actual URL

def reset_scales():
    driver.find_element(By.ID, "reset").click()
    time.sleep(2)

def weigh_bars(left_indices, right_indices):
    reset_scales()
    # Fill the left and right bowls
    print("Left_indices: ", left_indices)
    print("Right_indices: ", right_indices)
    for i, index in enumerate(left_indices):
        driver.find_element(By.ID, f"left_{i}").send_keys(str(index))
    for i, index in enumerate(right_indices):
        driver.find_element(By.ID, f"right_{i}").send_keys(str(index))
    # Click 'Weigh'
    driver.find_element(By.ID, "weigh").click()

    # Wait for the result and return it
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            element = driver.find_element(By.ID, "reset")
            if element.text != "?":  # Check if the text is not empty
                print(element.text)
                return element.text
        except NoSuchElementException:
            pass
        time.sleep(1)

    # If none of the expected texts are found, raise an exception or return a default value
    raise Exception("Unable to determine the result of weighing.")

def find_fake_bar():
    # Divide bars into three groups
    group1, group2, group3 = [0, 1, 2], [3, 4, 5], [6, 7, 8]

    # Weigh the first two groups
    result = weigh_bars(group1, group2)

    if result in ["<", ">"]:  # If either group is lighter, it contains the fake bar
        suspect_group = group1 if result == "<" else group2
    else:  # If they balance, the fake bar is in Group3
        suspect_group = group3

    # Weigh the first two bars in the suspect group
    result = weigh_bars([suspect_group[0]], [suspect_group[1]])

    print("group1: ", suspect_group[0])
    print("group2: ", suspect_group[1])
    print("result: ", result)

    if result in ["<", ">"]:  # If either bar is lighter, it's the fake one
        return suspect_group[0] if result == "<" else suspect_group[1]
    else:  # If they balance, the third bar is the fake one
        return suspect_group[2]

# Run the function and interact with the browser to confirm
fake_bar_index = find_fake_bar()

# Click on the suspected fake bar to verify
driver.find_element(By.ID, f"coin_{fake_bar_index}").click()

try:
    # Wait for the alert and verify the result
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = Alert(driver)
    alert_text = alert.text
    alert.accept()
    print(f"The fake gold bar is at index: {fake_bar_index}. Alert message: {alert_text}")
except NoAlertPresentException:
    print(f"No alert present after clicking on bar {fake_bar_index}. It may not be the fake bar.")


# for index in range(9):  # Assuming the buttons are numbered 0 to 8
#     # Click on the current index button
#     try:
#         print(f"Trying index: {index}")
#         button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.ID, f"coin_{index}"))
#         )
#         button.click()
#
#         # Wait for the alert and check the result
#         WebDriverWait(driver, 10).until(EC.alert_is_present())
#         alert = Alert(driver)
#         alert_text = alert.text
#         print(alert_text)
#         if "Yay! You find it!" == alert_text:
#             print(f"The fake gold bar is at index: {index}. Alert message: {alert_text}")
#             time.sleep(1)
#         alert.accept()  # Dismiss the alert before moving on to the next button
#         time.sleep(1)
#     except (NoAlertPresentException, TimeoutException):
#         print(f"No alert or incorrect alert after clicking on bar {index}. Trying the next bar.")

# Quit the browser after the operation
driver.quit()