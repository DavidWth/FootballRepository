from selenium import webdriver

browser = webdriver.Firefox()
browser.get("http://www.google.de")

assert "Google" in browser.title
print("OK")