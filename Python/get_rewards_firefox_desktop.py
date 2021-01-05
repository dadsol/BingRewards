import json
import random
import time
import getopt, sys
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import geckodriver_autoinstaller

geckodriver_autoinstaller.install()

def wait_for(sec=2):
    time.sleep(sec)


try:
  opts, args = getopt.getopt(sys.argv[1:],"hr:e:p:",["requests=","email=","password="])
except getopt.GetoptError:
  print ('get_rewards_firefox_desktop.py -r 60 -e <emailaddress> -p <password>')
  sys.exit(2)
searches = 1
for opt, arg in opts:
  print(opt+" = "+arg)
  if opt == '-h':
    print ('get_rewards_firefox_desktop.py -r 60 -e <emailaddress> -p <password>')
    sys.exit()
  elif opt in ("-e", "--email"):
    email = arg
  elif opt in ("-p", "--password"):
    password = arg
  elif opt in ("-r", "--requests"):
    searches = int(arg)
    
randomlists_url = "https://www.randomlists.com/data/words.json"
response = requests.get(randomlists_url)
words_list = random.sample(json.loads(response.text)['data'], searches)
print('{0} words selected from {1}'.format(len(words_list), randomlists_url))

profile = webdriver.FirefoxProfile()
options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options=options, firefox_profile=profile)

try:
    driver.get("https://login.live.com/")
    wait_for(10)
    elem = driver.find_element_by_name('loginfmt')
    elem.clear()
    elem.send_keys(email) # add your login email id
    driver.save_screenshot('/tmp/login1.png')
    elem.send_keys(Keys.RETURN)
    wait_for(5)
    elem1 = driver.find_element_by_name('passwd')
    elem1.clear()
    elem1.send_keys(password) # add your password
    driver.save_screenshot('/tmp/login2.png')
    elem1.send_keys(Keys.ENTER)
    wait_for(7)
    driver.save_screenshot('/tmp/login3.png')

 
except Exception as e:
    print(e)
    wait_for(4)


url_base = 'http://www.bing.com/search?q='

wait_for(5)

for num, word in enumerate(words_list):
    print('{0}. URL : {1}'.format(str(num + 1), url_base + word))
    try:
        driver.get(url_base + word)
        driver.save_screenshot('/tmp/sample_screenshot_'+str(num)+'.png')
        print('\t' + driver.find_element_by_tag_name('h2').text)
    except Exception as e1:
        print(e1)
    wait_for(5)
driver.close()
