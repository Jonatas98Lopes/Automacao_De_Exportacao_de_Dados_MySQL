from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
import os



class GoogleChrome:
    def __init__(self):

        self._chrome_options = Options()
        
        self._arguments = [
            '--lang=pt-BR',
            '--window-size=800,800',
            '--disable-notifications'
        ]

        for argument in self._arguments:
            self._chrome_options.add_argument(argument)

        self._experimental_options = {
            "download.default_directory": os.getcwd(),
            'download.prompt_for_download': False,
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_setting_values.automatic_downloads': 1,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False
        }

        self._chrome_options.add_experimental_option('prefs', 
        self._experimental_options)


        self._driver = webdriver.Chrome(service=ChromeService(), options=self._chrome_options)

        self._wait = WebDriverWait(
            driver=self._driver,
            timeout=40,
            poll_frequency=1,
            ignored_exceptions=[
                NoSuchElementException,
                ElementNotVisibleException,
                ElementNotVisibleException
            ])

    def get_driver(self):
        return self._driver
    
    def get_wait(self):
        return self._wait
    
    def get_arguments(self):
        return self._arguments
    
    def get_experimental_options(self):
        return self._experimental_options