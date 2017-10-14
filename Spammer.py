from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pickle , re , time
import json
import base64
import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg


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
        wait = WebDriverWait(self.driver, 120)
        y_arg = '//*[@id="side"]/div[2]/div/label/input'
        input_y = wait.until(EC.presence_of_element_located((By.XPATH, y_arg)))
        input_y.send_keys(contact + Keys.ENTER)
        input_box = self.driver.find_element_by_xpath(
            '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        for i in range(int(times)):
            input_box.send_keys(message + Keys.ENTER)

    def is_logged_in(self, timegiven=60):
        check = self.storage.get("WAToken1")
        wait = WebDriverWait(self.driver, timegiven)
        if check != None:
            try:
                y_arg = '//*[@id="side"]/div[2]/div/label/input'
                wait.until(EC.presence_of_element_located((By.XPATH, y_arg)))
                return True
            except TimeoutException:
                print("either not connected to the internet,or is logged out")
                return False
        else:
            return False

    def wait_till_login(self):
        wait = WebDriverWait(self.driver,300)
        try:
            y_arg = '//*[@id="side"]/div[2]/div/label/input'
            wait.until(EC.presence_of_element_located((By.XPATH, y_arg)))
            return True
        except TimeoutException:
            print("either not connected to the internet,or is logged out")
            return False

    def show_current_qr(self,src,fig):
        image64 = re.sub('^data:image/.+;base64,', '',src)
        image64 = base64.b64decode(image64)
        image64 = io.BytesIO(image64)
        image64 = mpimg.imread(image64, format='JPG')
        if fig==None:
            plt.ion()
            fig = plt.figure()
            plt.imshow(image64)
            plt.axis("off")
            plt.show()
        else:
            plt.imshow(image64)
        plt.pause(5.0)
        return fig

    def login_with_qr(self):
        self.storage.clear()
        self.driver.refresh()
        currentsrc = None
        currentfig = None
        wait = WebDriverWait(self.driver,30)
        while True:
            if self.storage.get('WAToken1') == None:
                reloadbutton = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div/div/div/div[1]/div[1]/div')))
                if(reloadbutton.get_attribute('class') == "idle"):
                    reloadbutton.click()
                imagelement = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div/div/div/div[1]/div[1]/div/img')))
                tmp = imagelement.get_attribute('src')
                if currentsrc == tmp:
                    time.sleep(1)
                    continue
                else:
                    currentsrc = tmp
                    if currentfig!=None:
                        plt.clf()
                    currentfig = self.show_current_qr(currentsrc,currentfig)
                    continue
            else:
                if currentfig!=None:
                    plt.close(currentfig)
                break


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
