from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pickle
import json

class Wspammer:
    def __init__(self):
        self.driver = webdriver.Chrome('chromedriver')
        self.driver.get('https://web.whatsapp.com')
        self.storage = LocalStorage(self.driver)

    def store_to_file(self, filename="default.ws"):
        if self.storage != None:
            to_store = self.storage.getAll()
            fileObject = open(filename, 'wb')
            pickle.dump(to_store, fileObject)

    def load_from_file(self, filename="default.ws"):
        if self.storage != None:
            fileObject = open(filename, 'r')
            storedict = pickle.load(fileObject)
            self.storage.setAll(storedict)
            self.driver.refresh()

    def spam_person(self, contact, message, times):
        wait = WebDriverWait(self.driver,120)
        y_arg = '//*[@id="side"]/div[2]/div/label/input'
        input_y = wait.until(EC.presence_of_element_located((By.XPATH, y_arg)))
        input_y.send_keys(contact + Keys.ENTER)
        input_box = self.driver.find_element_by_xpath(
            '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        for i in range(int(times)):
            input_box.send_keys(message + Keys.ENTER)

    def is_logged_in(self):
        check = self.storage.get("logout-token")
        wait = WebDriverWait(self.driver,60)
        if check!=None:
            try:
                y_arg = '//*[@id="side"]/div[2]/div/label/input'
                wait.until(EC.presence_of_element_located((By.XPATH, y_arg)))
                return True
            except TimeoutException:
                print("either not connected to the internet,or is logged out")
                return False
        else:
            return False


class LocalStorage:

    def __init__(self, driver):
        self.driver = driver

    def set(self, key, value):
        self.driver.execute_script(
            "window.localStorage.setItem('{}',{})".format(key, json.dumps(value)))

    def get(self, key=None):
        if key:
            return self.driver.execute_script(
                "return window.localStorage.getItem('{}')".format(key))
        else:
            return self.driver.execute_script("""
                    var items = {}, ls = window.localStorage;
                    for (var i = 0, k; i < ls.length; i++)
                      items[k = ls.key(i)] = ls.getItem(k);
                    return items;
                    """)

    def remove(self, key):
        self.driver.execute_script(
            "window.localStorage.removeItem('{}');".format(key))

    def clear(self):
        self.driver.execute_script(
            "window.localStorage.clear();")

    def getAll(self):
        toReturn = {}
        for key, value in self.get().items():
            toReturn[key] = value
        return toReturn

    def setAll(self, allKeys):
        for key, value in allKeys.iteritems():
            self.set(key, value)
