"""Usage: WhatsSpam.py
          WhatsSpam.py [--recipients=ListFile] [--message=MessageFile] [--skipcheck] [--times=NoOfTimes] [--delay=Seconds]

Options:
  -h --help                                   shows the help screen
  -r ListFile --recipients=ListFile           to import recipients from file
  -m MessageFile --message=MessageFile        to import message frome file
  -s --skipcheck                              to skip checks if right person is selected
  -t NoOfTimes --times=NoOfTimes              No Of Times To Send The Message
  -d Seconds --delay=Seconds                  delay between the messages in seconds(Default 0)
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib2,os,zipfile
import platform
from docopt import docopt
import time

def executeMultipleSpam():
    if(not(driverExeCheck())):
        exit()
    b = webdriver.Chrome("chromedriver")
    b.get('http://web.whatsapp.com')
    print "Log Into WhatsApp with the QRCode"
    raw_input("Press Any Key After Logging in")
    spamMultiple(b)
    b.close


def downloadFile(url):

    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print status,
    f.close()

def extractAndDelete(file_name):
    with zipfile.ZipFile(file_name,'r') as zfile:
        zfile.extractall()
    os.remove(file_name)

def askQuestions():

    if(not(arguments["--recipients"]==None) and os.path.isfile(arguments["--recipients"])):
        Names = getNamesFromFile(arguments["--recipients"])
    else:
        print "Please Insert Names Of People to be Spamed(Seperated by a ',' if Multiple Names)"
        Names = raw_input(">>>")
        Names = Names.split(',')

    if(arguments["--times"]==None):
        print "No of times to send the message?"
        Times = int(raw_input(">>>"))
    else:
        Times = int(arguments["--times"])

    if(not(arguments["--message"]==None) and os.path.isfile(arguments["--message"])):
        Message = readFromFile(arguments['--message'])
    else:
        print "What to Send Them?"
        Message = raw_input(">>>")

    return Names,Times,Message

def downloadChromeDriver():
    downloadFile("https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
    latest = open("LATEST_RELEASE","r")
    latestLINK = latest.read().replace("\n","")
    latest.close()
    os.remove("LATEST_RELEASE")
    driver = "http://chromedriver.storage.googleapis.com/"+ latestLINK +"/chromedriver_win32.zip"
    if(checkIfInClear(driver)):
        downloadFile(driver)
        extractAndDelete("chromedriver_win32.zip")
        return True
    else:
        return False

def checkIfInClear(driverLoc):
    print "Downloading Chrome Driver from " + driverLoc
    print "Do you agree to the Download (y/n)"
    ans = raw_input(">>>").lower()
    if(ans == 'y'):
        return True
    else:
        return False

def driverExeCheck():
        if(platform.system()=="Windows"):
            if (not (os.path.isfile('./chromedriver.exe'))):
                print "ChromeDriver.exe Not Found,Downloading It"
                if(not(downloadChromeDriver())):
                    print "Could Not Download the Driver Please Press Anykey to exit"
                    return False
        else:
            print "This is Not Usable on Your Machine Please Use a Windows One"
            raw_input("Press Anykey To Exit")
            return False
        return True


def spamGuy(b,Name,Times,Message):
    searchbar = b.find_element_by_xpath('//*[@id="side"]/div[2]/div/label/input')
    searchbar.clear()
    searchbar.click()
    searchbar.send_keys(Name)
    elem = b.find_element_by_xpath('//span[contains(text(),"%s")]' % Name)
    elem.click()
    if(not(arguments["--skipcheck"])):
        print "Please Check Weather The Correct Person Is Selected"
        raw_input("Press Any Key To Continue ")
    elem1 = b.find_elements_by_class_name('input')
    for i in range(0,Times):
        sendByLines(Message,elem1[1])
        elem1[1].send_keys('\n')
        if(not(arguments["--delay"]==None)):
            time.sleep(int(arguments["--delay"]))
    if(not(arguments["--skipcheck"])):
        raw_input("Press Any Key After The Messages Are Sent")
    else:
        time.sleep(2)

def sendByLines(Message,element):
    lineList = Message.splitlines()
    for line in lineList:
        element.send_keys(line)
        element.send_keys(Keys.SHIFT+Keys.ENTER)

def spamMultiple(b):
    Names,Times,Message = askQuestions()
    for name in Names:
        nameToUse = name.replace('\n', '').replace('\r', '')
        spamGuy(b,nameToUse,Times,Message)

def readFromFile(fileToRead):
    print "opening from %s" % fileToRead
    toRead = open(fileToRead,"r+")
    toReturn = toRead.read()
    return toReturn

def getNamesFromFile(filename):
    textInside = readFromFile(filename)
    nameList = textInside.replace('\r','').split('\n')
    for index,name in enumerate(nameList):
        if name=="":
            nameList.pop(index)
    print nameList
    return nameList

if __name__ == "__main__":
    arguments = docopt(__doc__)
    executeMultipleSpam()
