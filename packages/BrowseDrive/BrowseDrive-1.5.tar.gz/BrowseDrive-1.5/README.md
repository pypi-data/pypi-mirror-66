BrowseDrive is a package that allows for one to download the browser driver files used during browser automation with selenium. This package covers downloads for geckodriver and chromedriver. This package also has a module for the automation of browser drivers. 

#Installation
`pip3 install BrowseDrive==1.5`

#Usage
`import BrowseDrive
from BrowseDrive.driverautomator import DriverRunner
from BrowseDrive.driverdownloader import DriverDownloader`

#Downloading drivers 
`downloader = DriverDownloader() 
downloader.set_savepath("") # Save path goes inside here
downloader.download() # Starts the download process` 


#Automation of browser driver 
`runner = DriverRunner() 
runner.go("https://www.google.com") # Goes to Google.com
runner.search_elements("input","class", "classname")` 