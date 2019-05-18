# WhatsSpam

WhatsSpam is a python script to Send Multiple WhatsApp Messages To A 'Friend' Or A Group.

### Usage : 
    python whatsspam.py

### Dependencies
* [Python 2/3][python]
* [Selienum][selenium]
* [Chrome][chrome]
* [Matplotlib][matplotlib]

### How to contribute
All contributions are welcome, from code to documentation to bug reports. Please use GitHub to its fullest-- contribute Pull Requests, contribute tutorials or other wiki content-- whatever you have to offer, we can use it!

### Considerations in MacOs

For this error: ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1051)
Use: pip install certifi                                            
/Applications/Python\ 3.7/Install\ Certificates.command
In 3.7 use your python version.

For the error: selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome version must be between 70 and 73
  (Driver info: chromedriver=73.0.3683.68 (47787ec04b6e38e22703e856e101e840b65afe72),platform=Mac OS X 10.14.4 x86_64)
Use: brew cask upgrade chromedriver

### License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

### Disclaimer
***I take no responsibility for any harm caused by the usage of this script. Have fun!***

[selenium]:http://docopt.org/
[python]:https://www.python.org/downloads/
[chrome]:https://www.google.com/chrome/
[matplotlib]:https://matplotlib.org/
