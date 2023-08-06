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

