import os
import os.path as path
from colorama import Fore, Back, Style
from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

print(Style.RESET_ALL)

configPath = path.abspath(path.join(__file__ ,"../..")) + '\config.env'

def replaceLine(config_file, searchExp, replaceExp):
    with open(config_file, 'r') as file:
        data = file.readlines()
    isVarFound = False
    for index, line in enumerate(data):
        if searchExp in line:
            isVarFound = True
            data[index] = replaceExp + '\n'
            break
    if not isVarFound:
        data.append(replaceExp + '\n')
    with open(config_file, 'w') as file:
        file.writelines(data)


load_dotenv(configPath)
isCredentialsProvided = False

if os.getenv('HI10_USERNAME') is not None and os.getenv('HI10_USERNAME') != '' and os.getenv(
        'HI10_PASSWORD') is not None and os.getenv('HI10_PASSWORD') != '':
    isCredentialsProvided = True

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.maximize_window()
LOGIN_PAGE = 'https://hi10anime.com/wp-login.php'
browser.get(LOGIN_PAGE)

if isCredentialsProvided:
    try:
        WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.ID, "user_login"))
        ).send_keys(os.getenv('HI10_USERNAME'))
        WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.ID, "user_pass"))
        ).send_keys(os.getenv('HI10_PASSWORD'))
        WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.ID, "wp-submit"))
        ).click()
    except:
        pass

while True:
    cookie = browser.get_cookies()
    if len(cookie) > 0 and cookie[0]['name'] != 'wordpress_test_cookie' and cookie[0]['value'] != 'WP%20Cookie%20check':
        token = cookie[0]['name'] + ': ' + cookie[0]['value']
        browser.close()
        try:
            replaceLine(configPath, "LOGIN_TOKEN", 'LOGIN_TOKEN="' + token + '"')
            print('Imported token to config.env successfully!')
        except:
            print(
                'Failed to import token to config.env, Please copy paste the line to LOGIN_TOKEN Environmental Variable')
        print(Fore.RED + Back.WHITE + token)
        break
print(Style.RESET_ALL)
