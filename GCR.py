# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 11:16:31 2020

@author: Rushad
"""

import json
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, StaleElementReferenceException, NoSuchElementException

gcr_url = "https://accounts.google.com/signin/v2/identifier?service=classroom&passive=1209600&continue=https%3A%2F%2Fclassroom.google.com%2Fu%2F0%2Fh&followup=https%3A%2F%2Fclassroom.google.com%2Fu%2F0%2Fh&flowName=GlifWebSignIn&flowEntry=ServiceLogin"

chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--disable-notifications")

DRIVER_PATH = r"C:/chromedriver.exe"
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)

email = "rb3049@srmist.edu.in"
password = "SRMIST@#8930412"

def login(email, password):
    
    try:
    
        driver.get(gcr_url)
        
        email_id = driver.find_element_by_name('identifier')
        email_id.send_keys(email)
        submit_email_id = driver.find_element_by_id('identifierNext')
        submit_email_id.click()
        
        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
        pswd = password_field.find_element_by_tag_name('input')
        pswd.send_keys(password)
        submit_password = driver.find_element_by_id('passwordNext')
        submit_password.click()
    
        print("Login successfull \n")
        print("Logged in as {}".format(email))
    
    except ElementNotInteractableException or StaleElementReferenceException or NoSuchElementException:
        print("Login Failed")
    

def getDO():

    with open("acad_planner.json") as planner:
        planner_data = json.load(planner)
    
    date_time = datetime.datetime.now()
    month = date_time.month
    day = date_time.day
    day_order = planner_data[month-8][str(month)][str(day)]
    
    return day_order

def openLecture(slot):
    
    slot_dict = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "L1":7, "L2":8, "L3":9, "L4":10}
    
    with open("xpaths.json") as xpaths:
        xpath = json.load(xpaths)
    
    current_xpath = xpath[slot_dict[slot]][slot]["1"]
    subject = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, current_xpath)))
    subject.click()
    
    current_xpath = xpath[slot_dict[slot]][slot]["2"]
    link = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, current_xpath)))
    link.click()
    
    driver.switch_to.window(driver.window_handles[1])
    
    current_xpath = xpath[slot_dict[slot]][slot]["3"]
    join = WebDriverWait(driver,40).until(EC.element_to_be_clickable((By.XPATH, current_xpath)))
    join.click()


getDO()
login(email, password)
#gcr_home = driver.current_window_handle
#driver.switch_to.window(gcr_home)
openLecture("L4")