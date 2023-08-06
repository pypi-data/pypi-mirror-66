import platform
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pyvirtualdisplay import Display


def getPlatform(webdriver_path):
    print(webdriver_path)
    if platform.system() == 'Linux':
        print("LINUX-Platform")
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
    if platform.system() == 'Darwin':
        print("MAC-Platform")
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path=webdriver_path, options=options)
    return driver


def switchBrowser(count, path_to_driver):
    if count == 1:
        driver = webdriver.Firefox(executable_path=path_to_driver)
    elif count == 2:
        driver = webdriver.Chrome(executable_path=path_to_driver)
    elif count == 3:
        driver = webdriver.Safari(executable_path=path_to_driver)
    elif count == 4:
        driver = webdriver.Edge(executable_path=path_to_driver)
    return driver
