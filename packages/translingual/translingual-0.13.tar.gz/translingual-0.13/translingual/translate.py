from nltk.tokenize import sent_tokenize
import os
import itertools
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
import geckodriver_autoinstaller
    

from multiprocessing.pool import ThreadPool, Pool
import threading

geckodriver_autoinstaller.install()



class translate:
    def __init__(self, data, tolang, fromlang="en", thread=1, filename=None):
        self.data = data
        self.fromlang = fromlang
        self.tolang = tolang
        self.thread = thread
        self.threadLocal = threading.local()
        self.filename = filename

    def driver_create(self):
        driver = getattr(self.threadLocal, "driver", None)
        if driver is None:  # check if thread has it's driver
            options = FirefoxOptions()
            options.add_argument("--headless")
            driver = webdriver.Firefox(options=options, service_log_path=os.path.devnull)
            driver.get(
                f"https://translate.google.com/#view=home&op=translate&sl={self.fromlang}&tl={self.tolang}"
            )
            setattr(self.threadLocal, "driver", driver)
        return driver

    def translate(self):
        def trans_get(text):
            driver = self.driver_create()
            wait = WebDriverWait(driver, 10)
            input = wait.until(
                lambda driver: driver.find_element_by_xpath('//textarea[@id="source"]')
            )  # get input textarea if it exists
            input.send_keys(text)
            time.sleep(0.7)
            output = wait.until(
                lambda driver: driver.find_element_by_xpath(
                    '//span[@class="tlid-translation translation"]'
                )
            )  # get output if it exists
            c = output.text
            time.sleep(0.7)  # wait to avoiding repetated copy
            input.clear()
            if self.filename != None:
                if type(self.filename) == str:
                    with open(self.filename, "a") as f:
                        f.write(c + "\n")
                else:
                    filename = str(self.filename)
                    with open(self.filename, "a") as f:
                        f.write(c + "\n")
            else:
                return c

        if type(self.data) is list:
            return ThreadPool(self.thread).map(trans_get, self.data)
        elif type(self.data) is str:
            return ThreadPool(self.thread).map(trans_get, [self.data])
        else:
            try:
                return ThreadPool(self.thread).map(trans_get, self.text)
            except:
                pass

if __name__ == "__main__":
    trans=translate(data=["hello","terrible day here", "not so terrible day", "code to live", "I prefer to code"], fromlang="en", tolang="hy")
    print(trans.translate())