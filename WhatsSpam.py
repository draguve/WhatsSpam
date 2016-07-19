from selenium import webdriver
import urllib2,os,zipfile
import platform

def executeChromeWhatsapp():

    if(platform.system()=="Windows"):
        if (not (os.path.isfile('./chromedriver.exe'))):
            print "ChromeDriver.exe Not Found,Downloading It"
            downloadZipped("http://chromedriver.storage.googleapis.com/2.22/chromedriver_win32.zip")
    elif(platform.system()=="Darwin"):
        print "Please Use Firefox instead chrome is no supported right now."

    b = webdriver.Chrome("chromedriver")
    b.get('http://web.whatsapp.com')
    Name, Times, Message = askQuestions()
    elem = b.find_element_by_xpath('//span[contains(text(),"%s")]' % Name)
    elem.click()
    elem1 = b.find_elements_by_class_name('input')
    for i in range(0,Times):
        elem1[1].send_keys(Message)
        b.find_element_by_class_name('send-container').click()
    b.close()

def executeFireFoxWhatsapp():
    b = webdriver.Firefox()
    b.get('http://web.whatsapp.com')
    Name, Times, Message = askQuestions()
    elem = b.find_element_by_xpath('//span[contains(text(),"%s")]' % Name)
    elem.click()
    elem1 = b.find_elements_by_class_name('input')
    for i in range(0, Times):
        elem1[1].send_keys(Message)
        b.find_element_by_class_name('send-container').click()
    b.close()

def downloadZipped(url):

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
    with zipfile.ZipFile(file_name,'r') as zfile:
        zfile.extractall()
    os.remove(file_name)

def askQuestions():
    print "Log Into WhatsApp with the QRCode"
    raw_input("Press Any Key After Logging in")
    print ""
    print "Input Name Of Your 'Friend'"
    Name = raw_input(">>>")
    print ""
    print "No of times to send the message?"
    Times = int(raw_input(">>>"))
    print ""
    print "What to Send Them?"
    Message = raw_input(">>>")
    return Name,Times,Message


if __name__ == "__main__":
    print "what browser do you have installed?"
    print "Supported = Chrome,FireFox"
    browser = str.lower(raw_input(">>>"))
    if (browser == "chrome"):
        executeChromeWhatsapp()
    elif (browser == "firefox"):
        executeFireFoxWhatsapp()
    else:
        print "Your Browser is not supported"
