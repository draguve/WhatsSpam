from selenium import webdriver
import urllib.request, urllib.error, urllib.parse,os,zipfile
import platform

def executeChromeWhatsapp():

    if(platform.system()=="Windows"):
        if (not (os.path.isfile('./chromedriver.exe'))):
            print("ChromeDriver.exe Not Found,Downloading It")
            if(not(downloadChromeDriver())):
                print("Could Not Download the Driver Please Press Anykey to exit")
                exit()
    else:
        print("This is Not Usable on Your Machine Please Use a Windows One")
        input("Press Anykey To Exit")
        exit()
    b = webdriver.Chrome("chromedriver")
    b.get('http://web.whatsapp.com')
    Name, Times, Message = askQuestions()
    searchbar = b.find_element_by_xpath('//*[@id="side"]/div[2]/div/label/input')
    searchbar.click()
    searchbar.send_keys(Name)
    elem = b.find_element_by_xpath('//span[contains(text(),"%s")]' % Name)
    elem.click()
    print("Please Check Weather The Correct Person Is Selected")
    input("Press Any Key To Continue ")
    elem1 = b.find_elements_by_class_name('input')
    for i in range(0,Times):
        elem1[1].send_keys(Message)
        b.find_element_by_class_name('send-container').click()
    input("Press Any Key After The Messages Are Sent")
    b.close()

def downloadFile(url):

    file_name = url.split('/')[-1]
    u = urllib.request.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print("Downloading: %s Bytes: %s" % (file_name, file_size))

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
        print(status, end=' ')
    f.close()

def extractAndDelete(file_name):
    with zipfile.ZipFile(file_name,'r') as zfile:
        zfile.extractall()
    os.remove(file_name)

def askQuestions():
    print("Log Into WhatsApp with the QRCode")
    input("Press Any Key After Logging in")
    print("Input Name Of Your 'Friend'")
    Name = input(">>>")
    print("No of times to send the message?")
    Times = int(input(">>>"))
    print("What to Send Them?")
    Message = input(">>>")
    return Name,Times,Message

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
    print("Downloading Chrome Driver from " + driverLoc)
    print("Do you agree to the Download (y/n)")
    ans = input(">>>").lower()
    if(ans == 'y'):
        return True
    else:
        return False

if __name__ == "__main__":
    executeChromeWhatsapp()
