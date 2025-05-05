from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import sources
import time

seconds = 5

EMAIL = "contact.goclasses@gmail.com"
PASS = "QX2SzvpMd"

def process_link(link):
    q_id = link.split('/')[3]
    link = link + f"?state=edit-{q_id}"
    print(link)
    return link
    
def copy_QA(main_driver, link):
    main_driver.execute_script("window.open('');")
    main_driver.switch_to.window(main_driver.window_handles[1])
    main_driver.get(process_link(link))

    time.sleep(seconds)

    question = main_driver.find_element(By.XPATH, '//*[@id="q_content_ckeditor_data"]')
    question = question.get_attribute("value")
        
    try:
        selected_div = main_driver.find_element(By.CSS_SELECTOR, "div.qa-a-list-item.qa-a-list-item-selected")
        inner_html = selected_div.get_attribute("innerHTML")

        # Parse HTML and extract <p> tag
        soup = BeautifulSoup(inner_html, "html.parser")
        first_p = soup.find("p")
        answer = str(first_p) if first_p else "No <p> tag found"
    except Exception as e:
        answer = False
                
    print("\nQuestion : Fetched")
    print("Answer : Fetched", )
    return [question, answer]
    
def paste_Q(main_driver, question):
    wait = WebDriverWait(main_driver, 3)
    source_button = wait.until(EC.element_to_be_clickable((By.ID, "cke_32")))
    source_button.click()
        
    textarea = main_driver.find_element(By.NAME, "q_content")
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
                                """, textarea, question)
    time.sleep(seconds)

        
    submit_q = main_driver.find_element(By.XPATH, '//*[@type="submit"]')
    submit_q.click()
    time.sleep(seconds)
        
def paste_A(main_driver, answer):
    #open button
    submit_ans = main_driver.find_element(By.XPATH, '//*[@id="q_doanswer"]')
    submit_ans.click()
    time.sleep(seconds)
    
    wait = WebDriverWait(main_driver, 3)
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
    time.sleep(seconds)
    
    #paster answer
    button = main_driver.find_element(By.CSS_SELECTOR, 'button.qa-form-tall-button.qa-form-tall-button-answer')
    button.click()
    
    
def paste_QA(main_driver, tar_link, question, answer):
    main_driver.execute_script("window.open('');")
    main_driver.switch_to.window(main_driver.window_handles[2])
    main_driver.get(process_link(tar_link))
    
    paste_Q(main_driver, question)
    if answer:
        paste_A(main_driver, answer)
    
    time.sleep(seconds)

def fun(main_driver):
    for idx, (link, tar_link) in enumerate(zip(sources.source, sources.target_source)):
        # Open a new tab
        print("\nQuestion: ", idx+1)
        question, answer = copy_QA(main_driver, link)
        paste_QA(main_driver, tar_link, question, answer)

def login():
    link = "https://gateoverflow.in/login?to="
    main_driver = webdriver.Chrome()
    main_driver.get(link)
    
    time.sleep(seconds)
    
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
