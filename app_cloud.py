from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
import pyperclip
import streamlit as st
import time
import selenium

print(selenium.__version__)

# install driver
@st.cache_resource
def get_driver():
    return webdriver.Chrome(
        service=Service(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        ),
        options=options,
    )

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--headless")

driver = get_driver()

st.title("Hello, Eng Mahmoud")
st.write("❤️ أجمد مهندس في العالم ربنا يحفظك")
st.markdown('---')

username = str(st.secrets.username)




# login
driver.get('https://demi.ischooltech.com/login/tutor')
WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)
driver.find_element('id', 'Email ID').send_keys(username)
driver.find_element('id', 'exampleFormControlInput1').send_keys(username)
driver.find_element('class name', 'button.button-color-primary.w-100.rounded-pill.font_16.font-semibold.mt-4.m-auto.button-size-med').click()

time.sleep(2)

# filtering
filter = 'd-flex.cursor-pointer.border.font-color-blue300.rounded.text-nowrap.text-start.gap-2.flex-1.align-items-center.ps-10'
filter_btn = 'select-option-button.text-start.text-capitalize.cursor-pointer.font-color-blue600'


filters = driver.find_elements('class name', filter)
filters[0].click()
driver.find_elements('class name', filter_btn)[0].click() # today

filters[1].click()  
driver.find_elements('class name', filter_btn)[0].click()  # offline

time.sleep(2)


# get student list
std_name = 'font_16.font-light.font-color-blue600.line-clamp-1'
std_id = 'mb-0 font_14 font-light font-color-blue300.line-clamp-1.text-start'
std_login_url_btn = 'button.gap-2.align-items-center.button-text-orange500.font_14.mt-1.mb-1.font-normal.py-02.px-0.justify-content-start'

def get_student_list(name, id, login_btn):
    time.sleep(2)
    names = driver.find_elements('class name', name)
    ids = driver.find_elements('class name', id)
    urls = driver.find_elements('class name', login_btn)

    print(len(names), len(ids), len(urls))

    student_list = []
    for i in range(len(names)):

        counter = 1
        while counter <= 7:
            try:
                urls[i].click()
                break
            except Exception as e:
                print(f"Error clicking link: {e}, retrying {counter}...")
                counter += 1
                time.sleep(1)

        student_list.append({
            'name': names[i].text,
            'id': 'ids[i].text',
            'login_url': pyperclip.paste()
        })
    
    return student_list


def create_student_container(student):
    containter = st.container(border = True)
    containter.write(f'Name: {student["name"]}')
    containter.write(f'ID: {student["id"]}')
    containter.link_button("Login to iSchool", student['login_url'])

navigate_btns = 'button.gap-2.align-items-center.button-border.button-border-primary.border-0.font_14.p-0'

while True:
    student_list = get_student_list(std_name, std_id, std_login_url_btn)
    
    for student in student_list:
        create_student_container(student)

    # navigate to next page
    if driver.find_elements('class name', navigate_btns)[1].is_enabled():
        driver.find_elements('class name', navigate_btns)[1].click()
        print('clicked')
    else:
        break


time.sleep(5) 
driver.close()

