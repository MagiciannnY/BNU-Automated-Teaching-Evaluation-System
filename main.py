from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

name = input("Enter your username:")
pwd = input("Enter your password:")

option = webdriver.ChromeOptions()
option.add_argument('--start-maximized')
option.add_argument("--disable-gpu")

option.add_experimental_option('excludeSwitches', ['enable-automation'])

prefs = {'profile.default_content_settings.popups': 0,
         'profile.default_content_setting_values.automatic_downloads': 1}
option.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(options=option)

wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

driver.maximize_window()
driver.set_page_load_timeout(60)
url = "https://ss.bnu.edu.cn/www/dd/vue/spa/pjxt#/xspj?type=qmpj"
driver.get(url)

driver.implicitly_wait(10)
time.sleep(3)
username = driver.find_element(By.ID, "un")
username.send_keys(name)

password = driver.find_element(By.ID, "pd")
password.send_keys(pwd)

submit = driver.find_element(By.ID, "index_login_btn")
submit.click()

MAX_TABS = 2

while True:
    all_tabs = driver.window_handles
    if len(all_tabs) > MAX_TABS:
        driver.switch_to.window(all_tabs[0])
        driver.close()
        driver.switch_to.window(all_tabs[-1])
    driver.refresh()
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'app')))
    time.sleep(2)

    pending_tab = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[1]/div/div/div/div[2]/span')
    pending_tab.click()
    time.sleep(1)

    courses = driver.find_elements(By.CLASS_NAME, "pjxt-com-xspjList")
    print(courses)
    if courses.__len__() == 0:
        break
    course = courses[0]

    print(course.get_attribute('outerHTML'))

    button = course.find_element(By.XPATH, './/div[2]/div[2]')
    print(button.get_attribute('outerHTML'))

    driver.execute_script("arguments[0].click();", button)

    time.sleep(1)
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'corebody')))

    radio_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")
    for i in range(10):
        time.sleep(0.5)
        label = driver.find_element(By.XPATH, f"//label[@for='mini-{15 + 2 * i}$ck$0']")
        label.click()

    time.sleep(1)

    for i in range(1, 6):
        driver.execute_script(f"window.scrollBy(0, {400 * i})")
        time.sleep(0.5)
    time.sleep(1)

    submit_button = driver.find_element(By.ID, 'cea66e38-e08b-4585-997a-be3216539a5d_as')
    submit_button.click()
    time.sleep(0.5)

    alert = Alert(driver)
    alert.accept()

    time.sleep(1)
    driver.refresh()

print("已结束评教")

driver.quit()
