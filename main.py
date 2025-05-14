'''
-1 : Not able to copy
False: Exception occured in respective block
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import Url
import time

DELAY = 3
EMAIL = ""
PASS = ""
TRY = 1


def process_link(link):
    q_id = link.split('/')[3]
    link = link + f"?state=edit-{q_id}"
    return link
    
def copy_Q(main_driver, link):
    try:
        question = main_driver.find_element(By.XPATH, '//*[@id="q_content_ckeditor_data"]')
        question = question.get_attribute("value")
    except Exception as e:
        print("Error: Not able to Copy Question")
        if TRY :
            print("Attempting again.")
            question = -1 #No Valid Question copied
            copy_Q(main_driver, link)
            TRY = TRY - 1
    return question
    
def copy_A(main_driver, link):  
    try:
        selected_div = main_driver.find_element(By.CSS_SELECTOR, "div.qa-a-list-item.qa-a-list-item-selected")
        inner_html = selected_div.get_attribute("innerHTML")
        soup = BeautifulSoup(inner_html, "html.parser")
        first_p = soup.find("p")
        if first_p:
            answer = str(first_p) #Valid ansewer copied
        else:
            answer = -1 #No valid ansewer copied
            print("Error: Did not get any Answer. TRY: ", TRY)
    except Exception as e:
        print("Error: Not able to Copy Answer")
        if TRY:
            print("Attempting again.")
            answer = -1 #No valid ansewer copied
            copy_Q(main_driver, link)
            TRY = TRY - 1
    return answer
    
def paste_Q(main_driver, question):
    try:
        wait = WebDriverWait(main_driver, DELAY)
        source_button = wait.until(EC.element_to_be_clickable((By.NAME, "q_doedit")))
        source_button.click()
        
        wait = WebDriverWait(main_driver, DELAY)
        source_button = wait.until(EC.element_to_be_clickable((By.ID, "cke_32")))
        source_button.click()
            
        textarea = main_driver.find_element(By.NAME, "q_content")
        main_driver.execute_script("""
                                        var content = arguments[1];
                                        var textarea = arguments[0];
                                        if (window.CKEDITOR) {
                                            for (var name in CKEDITOR.instances) {
                                                if (CKEDITOR.instances[name].element.$ === textarea) {
                                                    CKEDITOR.instances[name].setData(content);
                                                    break;
                                                }
                                            }
                                        }
                                        textarea.value = content;
                                    """, textarea, question)
        time.sleep(DELAY)
        submit_q = main_driver.find_element(By.XPATH, '//*[@type="submit"]')
        submit_q.click()
        time.sleep(DELAY)
    except Exception as e:
        print("Error: Not able to Paste Question. TRY: ", TRY)
        if TRY:
            print("Attempting again.")
            paste_Q(main_driver, question)
            TRY = TRY - 1
        
def paste_A(main_driver, answer):
    try:
        submit_ans = main_driver.find_element(By.XPATH, '//*[@id="q_doanswer"]')
        submit_ans.click()
        time.sleep(DELAY)
        
        wait = WebDriverWait(main_driver, DELAY)
        source_button = wait.until(EC.element_to_be_clickable((By.ID, "cke_32")))
        source_button.click()
            
        textarea = main_driver.find_element(By.NAME, "a_content")
        # Paste the value using JS (works even if hidden)
        main_driver.execute_script("""
                                        var content = arguments[1];
                                        var textarea = arguments[0];
                                        if (window.CKEDITOR) {
                                            for (var name in CKEDITOR.instances) {
                                                if (CKEDITOR.instances[name].element.$ === textarea) {
                                                    CKEDITOR.instances[name].setData(content);
                                                    break;
                                                }
                                            }
                                        }
                                        textarea.value = content;
                                    """, textarea, answer)
        time.sleep(DELAY)
            button = main_driver.find_element(By.CSS_SELECTOR, 'button.qa-form-tall-button.qa-form-tall-button-answer')
        button.click()
        time.sleep(DELAY)
    except Exception as e:
        print("Error: Not able to Paste Answer. TRY: ", TRY)
        if TRY:
            print("Attempting again.")
            paste_A(main_driver, answer)
            TRY = TRY - 1
    
def copy_QA(main_driver, link):
    main_driver.execute_script("window.open('');")
    main_driver.switch_to.window(main_driver.window_handles[1])
    main_driver.get(link)
    
    question = copy_Q(main_driver, link)
    if question != -1:
        answer = copy_A(main_driver, link) #copy answer only when question successfuly copied
    else:
        answer = -1

    time.sleep(DELAY)
    return [question, answer]

def paste_QA(main_driver, tar_link, question, answer):
    main_driver.execute_script("window.open('');")
    main_driver.switch_to.window(main_driver.window_handles[2])
    main_driver.get(tar_link)
    
    paste_Q(main_driver, question)
    if answer != -1:
        paste_A(main_driver, answer)
    else:
        print("Mark: Answer is not copied")
    
    time.sleep(DELAY)
    

def fun(main_driver):
    for idx, (link, tar_link) in enumerate(zip(Url.source, Url.target)):
        # Open a new tab
        print("\nQuestion: ", idx+1)
        question, answer = copy_QA(main_driver, link)
        if question != -1:
            paste_QA(main_driver, tar_link, question, answer)
        else:
            print("Question: %d, Failed !" %(idx))

def login():
    link = "https://gateoverflow.in/login?to="
    main_driver = webdriver.Chrome()
    main_driver.get(link)
    
    time.sleep(DELAY)
    
    username = main_driver.find_element(By.XPATH, f'//*[@id="emailhandle"]')
    password = main_driver.find_element(By.XPATH, f'//*[@id="password"]')
    
    username.send_keys(EMAIL)
    password.send_keys(PASS)
    
    log_in = main_driver.find_element(By.XPATH, '//*[@type="submit"]')
    log_in.click()
    
    return main_driver


if __name__ == '__main__':
    main_driver = login()
    time.sleep(seconds)
    fun(main_driver)
    main_driver.quit()
