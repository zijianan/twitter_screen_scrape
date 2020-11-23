import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from datetime import datetime,timedelta,timezone
import time
from webdriver_manager.chrome import ChromeDriverManager
import pickle
import argparse
import pandas as pd
import numpy as np
import sys
from tqdm import tqdm
import json
import glob
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from tqdm.autonotebook import tqdm
import pickle
import os
import codecs
from lxml import etree
from lxml import html
from lxml import html
from datetime import datetime
from collections import Counter
import string
from datetime import datetime
tqdm.pandas()
import random
from shutil import copyfile
from os import path


user = {'user1':'pwd1'}
global account_flag
account_flag = {'user1':'active_dem'}

ap = argparse.ArgumentParser()
ap.add_argument(
    "-md","--md",default='0')
args = vars(ap.parse_args())
md = str(args['md'])

options = Options()

options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_argument("--mute-audio")
options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("headless")
prefs = {
    'profile.default_content_setting_values' : {
        'images' : 2
    }
}

driver = webdriver.Chrome(
    executable_path=ChromeDriverManager().install(), options=options)
driver.maximize_window()
for i in range(len(user)):
    driver.execute_script("window.open('');")
for i in range(1,len(user)+1): 
    driver.switch_to.window(driver.window_handles[i])


time.sleep(0.5)


# adem ndem arep nrep fot nfot


def screen_scrape(user,ongoing_id,ongoing_screenname,data):
    windowsNumber = [n+1 for n in range(len(user))]
    
    for account,i in zip(user,windowsNumber):
        driver.switch_to.window(driver.window_handles[i])
        time.sleep(0.1)

        driver.get('https://twitter.com/login')
        time.sleep(0.3)
        try:
            driver.find_element_by_xpath('//*[@id="doc"]/div/div[1]/div[1]/div[1]/form/input[1]').click()
        except:
            pass
        time.sleep(0.2)
        trylogin(account,user[account])
        time.sleep(0.1)
        website = 'https://twitter.com/'+ongoing_screenname+'/status/'+ongoing_id
        driver.get(website)
        time.sleep(0.5)
        driver.execute_script("document.body.style.zoom='25%'")
        for i in range(6):
            driver.execute_script("window.scrollTo(0, 1080)")
            time.sleep(0.3)
    
        
        time.sleep(0.3)
        data = htmlpaser(data,ongoing_id,account_flag[account],ongoing_screenname)
        # driver.execute_script("window.scrollTo(0, 2160)") 

        driver.delete_all_cookies()
        driver.execute_script("document.body.style.zoom='100%'")
    return data
def trylogin(account,password):
    if driver.current_url == 'https://twitter.com/logout/error':
        error_logout(account,password)
    else:
        driver.find_element_by_name('session[username_or_email]').send_keys(account)
        time.sleep(0.1)
        driver.find_element_by_name('session[password]').send_keys(password)
        time.sleep(0.1)
        driver.find_element_by_xpath("//div[@data-testid='LoginForm_Login_Button']").click()
        time.sleep(0.3)
    
def error_logout(account,password):
    driver.find_element_by_xpath("//*[text()='Log out']").click()
    time.sleep(1)
    driver.get('https://twitter.com/login')
    trylogin(account,password)



def htmlpaser(data,tid,account_name,ongoing_screenname):
    names = ongoing_screenname
    # time = 'NA'
    root = html.fromstring(driver.page_source).getroottree()
    first_layer = root.xpath("//div[@aria-label = 'Timeline: Conversation']")[0]
    first_layer_tree = etree.fromstring(etree.tostring(first_layer))
    url_list = first_layer_tree.xpath('//a/@href')
    repliers_urls = []
    repliers = []
    for url_e in url_list:
        if ongoing_screenname not in url_e and 'status' in url_e:
            url_split = list(url_e)
            url_split_counter = Counter(url_split)
            if url_split_counter['/'] == 3:
                repliers_urls.append(url_e)
    for repliers_url in repliers_urls:
        repliers.append(repliers_url.split('/')[1].split('/status/')[0])
    scrape_date = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
    for i in range(len(repliers_urls)):
        data = data.append({'name':names,'tid': tid, 'url':'https://twitter.com'+repliers_urls[i],\
                                            'account':account_name,\
                                            'scrape_date':scrape_date},ignore_index=True) 
    return data

def queue(ongoing_id, ongoing_user, ongoing_time,queueline,data):
    priority=[]
    for id,target,otime in zip(ongoing_id,ongoing_user,ongoing_time):
        for i in range(6):
            delta = timedelta(minutes=i*10)
            time = str(datetime.strptime(otime, '%Y-%m-%d %H:%M:%S') + delta)
            minute = time[14:16]
            hour = time[11:13]
            day = time[8:10]
            month = time[5:7]
            quelabel = int(minute)+int(hour)*100+int(day)*10000+int(month)*1000000
            if i == 0:
                priority.append((id,target,quelabel))
            else:
                queueline.append((id,target,quelabel))
    Sort_Tuple(queueline)
    print("woking on priority",priority)
    print("now is", str(datetime.now(timezone.utc)))
    print("the remaining",queueline)
    for subpriority in priority:
        data = screen_scrape(user,subpriority[0],subpriority[1],data)
    return queueline,data

def check_new(queueline,data):
    while True:
        old = os.path.getsize('old_out.csv')
        new = os.path.getsize('new_out.csv')
        if new > old:
            oldoutfile = pd.read_csv('old_out.csv',dtype=str,index_col=False)
            newoutfile = pd.read_csv('new_out.csv',dtype=str,index_col=False)
            df = pd.concat([oldoutfile, newoutfile]).drop_duplicates(keep=False)
            print("woking on",df.date.values,df.tid.values)
            print("now is", str(datetime.now(timezone.utc)))
            queueline,data = queue(list(df.tid.values),list(df.user.values),list(df.date.values),queueline,data)
            copyfile('new_out.csv','old_out.csv')

            # time.sleep(10)
        else:
            if len(queueline)!=0:
                now = str(datetime.now(timezone.utc))
                minute = now[14:16]
                hour = now[11:13]
                day = now[8:10]
                month = now[5:7]
                nowlabel = int(minute)+int(hour)*100+int(day)*10000+int(month)*1000000
                absnumber = abs(nowlabel - queueline[0][2])
                if nowlabel - queueline[0][2] > 0 or absnumber <= 1:
                    if len(queueline) == 1:
                        print("woking on",queueline[0])
                        print("now is", str(datetime.now(timezone.utc)))
                    else:
                        print("woking on",queueline[0])
                        print("now is", str(datetime.now(timezone.utc)))
                        print("the remaining",queueline[1:])
                    data = screen_scrape(user,queueline[0][0],queueline[0][1],data)
                    queueline.pop(0)
            time.sleep(10)
        now = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
        data.to_csv('real_time_collection/'+str(now)+'.csv',index=False)
        data = pd.DataFrame(columns=['name','tid', 'url', 'scrape_date'])


def Sort_Tuple(tup):  
  
    # reverse = None (Sorts in Ascending order)  
    # key is set to sort using second element of  
    # sublist lambda has been used  
    tup.sort(key = lambda x: x[2])  
    return tup 

if md != 'real-time':
    if not path.exists('collection'):
        os.mkdir('collection')
    obj_list = pd.read_csv('obj_list.csv',dtype=str,index_col=False)
    data = pd.DataFrame(columns=['name','tid', 'url', 'account', 'scrape_date'])  
    for index,row in tqdm(obj_list.iterrows(), total=obj_list.shape[0]):
        data = screen_scrape(user,row['tid'],row['screen_name'],data)  
        if len(data) >= 10000:
            now = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
            data.to_csv('collection/'+str(now)+'.csv',index=False)
            data = pd.DataFrame(columns=['name','tid', 'url', 'account', 'scrape_date'])
    now = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
    data.to_csv('collection/'+str(now)+'.csv',index=False)
    driver.close()

else:
    if not path.exists('real_time_collection'):
        os.mkdir('real_time_collection')
    ini_csv = pd.DataFrame(columns=['date','user','is_retweet','is_quote','tid'])
    ini_csv.to_csv('old_out.csv',index=False)
    data = pd.DataFrame(columns=['name','tid', 'url', 'account', 'scrape_date'])
    queueline = []
    check_new(queueline,data)


