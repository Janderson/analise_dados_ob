# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
driver = webdriver.Firefox()
driver.get("https://bancdebinary.com/pt-br/")
#assert "24option" in driver.title
print "site ok"
sleep(2)

def login_bb():
	user = driver.find_element_by_id("loginEmailTop")
	user.send_keys("democontatoocaradeti@gmail.com")
	e_pass = driver.find_element_by_id("loginPassTop")
	e_pass.send_keys("helloword")

	e_pass.send_keys(Keys.RETURN)
	#assert "No results found." not in driver.page_source
	sleep(5)
	
def login_24opt():
	user = driver.find_element_by_class_name("navigation_menu_username_field")
	user.send_keys("jande2")
	e_pass = driver.find_element_by_class_name("navigation_menu_password_field")
	e_pass.send_keys("H2ll0w0rd2")

	e_pass.send_keys(Keys.RETURN)
	#assert "No results found." not in driver.page_source
	sleep(5)
	#driver.close()


login_bb()
