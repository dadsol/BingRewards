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
  opts, args = getopt.getopt(sys.argv[1:],"hdmr:e:p:",["mobile","requests=","email=","password=","debug"])
except getopt.GetoptError:
  print ('get_rewards_firefox_desktop.py -r 60 -e <emailaddress> -p <password>')
  sys.exit(2)
searches = 1
debug = False
mobile = False
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
  elif opt in ("-d", "--debug"):
    debug = True
  elif opt in ("-m", "--mobile"):
    mobile = True
    
randomlists_url = "https://www.randomlists.com/data/words.json"
response = requests.get(randomlists_url)
words_list = random.sample(json.loads(response.text)['data'], searches)
print('{0} words selected from {1}'.format(len(words_list), randomlists_url))

profile = webdriver.FirefoxProfile()
if mobile:
    ua = "Mozilla/5.0 (Android 6.0.1; Mobile; rv:77.0) Gecko/77.0 Firefox/77.0"
else:
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43"
profile.set_preference("general.useragent.override",ua)
options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options=options, firefox_profile=profile)

try:
    driver.get("https://login.live.com/")
    wait_for(5)
    elem = driver.find_element_by_name('loginfmt')
    elem.clear()
    elem.send_keys(email) # add your login email id
    if debug:
        driver.save_screenshot('/tmp/login1.png')
    elem.send_keys(Keys.RETURN)
    wait_for(2)
    elem1 = driver.find_element_by_name('passwd')
    elem1.clear()
    elem1.send_keys(password) # add your password
    if debug:
        driver.save_screenshot('/tmp/login2.png')
    elem1.send_keys(Keys.ENTER)
    wait_for(5)
    if debug:
        driver.save_screenshot('/tmp/login3.png')

except Exception as e:
    print(e)
    wait_for(4)

url_base = 'http://www.bing.com/search?q='

for num, word in enumerate(words_list):
    print('{0}. URL : {1}'.format(str(num + 1), url_base + word))
    try:
        wait_for(3)
        driver.get(url_base + word)
        if debug:
            driver.save_screenshot('/tmp/search_for_'+word+'_'+str(num)+'.png')
        print('\t' + driver.find_element_by_tag_name('h2').text)
    except Exception as e1:
        print(e1)
driver.close()
