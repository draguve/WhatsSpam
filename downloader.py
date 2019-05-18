import urllib.request, urllib.error, urllib.parse
import os
import zipfile
import platform
from os import path

def downloadFile(url):
    file_name = url.split('/')[-1]
    u = urllib.request.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    ## getheader deprecated in python3, use get() instead for HTTPMessage
    ## https://github.com/sklarsa/django-sendgrid-v5/pull/34
    # file_size = int(meta.getheaders("Content-Length")[0])
    file_size = int(meta.get("Content-Length")[0])
    print("Downloading: %s Bytes: %s" % (file_name, file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (
            file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print(status, end=' ')
    f.close()

def extractAndDelete(file_name):
    with zipfile.ZipFile(file_name, 'r') as zfile:
        zfile.extractall()
    os.remove(file_name)

def check_if_agree(driverLoc):
    print("Downloading Chrome Driver from " + driverLoc)
    print("Do you agree to the Download (y/n)")
    ans = input(">>>").lower()
    if(ans == 'y' or ans == 'Y'):
        return True
    else:
        return False

def check_for_driver():
    system = platform.system()
    if system == 'Windows':
        if(not(os.path.isfile('./chromedriver.exe'))):
            downloadChromeDriver(system)
    elif system == 'Linux':
        if(not(os.path.isfile('./chromedriver'))):
            downloadChromeDriver(system)
    elif system == 'Darwin':
        if(not(os.path.isfile('./chromedriver'))):
            downloadChromeDriver(system)
    else:
        print('The so is {0}'.format(system))
        print("Driver not available for your system")
        exit()

def downloadChromeDriver(system):
    if system == 'Windows':
        filename = "chromedriver_win32.zip"
    elif system == "Linux":
        filename = "chromedriver_linux32.zip"
    elif system == 'Darwin':
        filename = "chromedriver_mac64.zip"
    downloadFile(
        "https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
    latest = open("LATEST_RELEASE", "r")
    latestLINK = latest.read().replace("\n", "")
    latest.close()
    os.remove("LATEST_RELEASE")
    driver = "http://chromedriver.storage.googleapis.com/" + latestLINK + "/" + filename
    if(check_if_agree(driver)):
        downloadFile(driver)
        extractAndDelete(filename)
        return True
    else:
        return False
