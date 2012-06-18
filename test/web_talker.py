from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Firefox() # Get local session of firefox
browser.get("http://www.kyozou.com/index.php/main/login-seller.html?UserName=cwhiteside&Password=stspassword&pw=1&login=Submit+Query") # Load page
#UserName=cwhiteside&Password=stspassword&pw=1&login=Submit+Query
assert "Kyozou" in browser.title
un = browser.find_element_by_name("UserName")
pw = browser.find_element_by_name("Password")
un.send_keys("cwhiteside" + Keys.TAB)
un.send_keys("stspassword" + Keys.TAB)
clickAndWait("pw")
time.sleep(0.2) # Let the page load, will be added to the API
try:
	print "whoa"
	#browser.find_element_by_xpath("//a[contains(@href,'http://seleniumhq.org')]")
except NoSuchElementException:
	assert 0, "can't find seleniumhq"
browser.close()