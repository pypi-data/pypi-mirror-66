from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def cicle(count, path_to_driver):
    if count == 1:
        driver = webdriver.Firefox(executable_path=path_to_driver)
    elif count == 2:
        driver = webdriver.Chrome(executable_path=path_to_driver)
    elif count == 3:
        driver = webdriver.Safari(executable_path=path_to_driver)
    elif count == 4:
        driver = webdriver.Edge(executable_path=path_to_driver)
    return driver


def switchTo(name, path_to_driver, headless=False):
    if name == 'Firefox':
        driver = webdriver.Firefox(executable_path=path_to_driver)
    elif name == 'Chrome':
        driver = webdriver.Chrome(executable_path=path_to_driver)
    elif name == 'Safari':
        driver = webdriver.Safari(executable_path=path_to_driver)
    elif name == 'Edge':
        driver = webdriver.Edge(executable_path=path_to_driver)
    return driver
