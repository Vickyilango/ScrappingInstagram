#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 17:55:58 2019

@author: VIGNESHWAR.I
"""



#finding who likes
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
import pandas as pd
import time
import rouigram as instagram

#get_post_likers('B0xaWBmAi7L')


def get_post_likers(shortcode):
    driver.get('https://www.instagram.com/p/'+shortcode+'/')
    driver.execute_script("window.scrollTo(0, 1080)") 
    url = "/p/" + shortcode + "/liked_by/"
    time.sleep(2)
    #like_link = driver.find_element_by_xpath('//a[@href="'+url+'"]')
    
    python_button = driver.find_elements_by_xpath("//button[@class='_0mzm- sqdOP yWX7d    _8A5w5    ']")[0]
    python_button.click()
    #_0mzm- sqdOP yWX7d    _8A5w5    
    #like_link.click()
    time.sleep(2)
    users = []
    pb = driver.find_element_by_xpath("//div[@role = 'dialog']/div[2]/div[1]/div[1]").value_of_css_property("padding-bottom")
    match = False
    while match==False:
        lastHeight = pb

        # step 1
        elements = driver.find_elements_by_xpath("//*[@id]/div/a")
        # step 2
        for element in elements:
            if element.get_attribute('title') not in users:
                users.append(element.get_attribute('title'))
        # step 3
        driver.execute_script("return arguments[0].scrollIntoView();", elements[-1])
        time.sleep(1)
        # step 4
        pb = driver.find_element_by_xpath("//div[@role = 'dialog']/div[2]/div[1]/div[1]").value_of_css_property("padding-bottom")
        if lastHeight==pb or len(users) >= 1500:
            match = True
    return users

#get commenters
def get_commenters():
    driver.get('https://www.instagram.com/p/BuE82VfHRa6/')
    
    
    elems = driver.find_elements_by_xpath("//a[@class='FPmhX notranslate TlrDj']")
    
    users = []
    
    for elem in elems:
        users.append(elem.get_attribute('title'))
        print('Title : ' +elem.get_attribute('title'))
    
    return users

#Get picture links
def get_pic_links():
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(ChromeDriverManager().install())
        #driver.get('https://www.instagram.com/explore/tags/nnnow/')
        driver.get('https://www.instagram.com/heynnnow/')
        
        SCROLL_PAUSE_TIME = 2
        
        final = []
        while True:
        
            # Get scroll height
            ### This is the difference. Moving this *inside* the loop
            ### means that it checks if scrollTo is still scrolling 
            last_height = driver.execute_script("return document.body.scrollHeight")
        
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            elems = driver.find_elements_by_xpath("//a[@href]")
            for elem in elems:
                final.append(elem.get_attribute("href"))
        
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
        
                # try again (can be removed)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
        
                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
        
                # check if the page height has remained the same
                if new_height == last_height:
                    # if so, you are done
                    break
                # if not, move on to the next loop
                else:
                    last_height = new_height
                    continue
        
        elems = driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            final.append(elem.get_attribute("href"))
        
        picture_links = set([i for i in final if '/p/' in i ])
        picture_links = list(picture_links)
        shortcodes = [ i.split('/p/')[-1].split('/')[0] for i in picture_links ]
        return shortcodes


def main(d,shortcodes,total):
    dict1 = {}
    for i in shortcodes:
        print(total)
        total = total - 1
        try:
            listofusers = get_post_likers(i)
            dict1[i] = listofusers
            temp = pd.DataFrame({'Shortcode': i, 'Listofusers':listofusers })
            d = pd.concat([d, temp])
        except:
            continue
    return d


#Get user details

def get_user_details(userbase,d2):
    lenuser = len(userbase)
    for i in userbase:
        print(lenuser)
        lenuser = lenuser - 1
        try:
            print('inside')
            info = instagram.getInformation(i)
            userid = instagram.getInformation.user_id(info)  # You will get user id
            username = instagram.getInformation.username(info) # You will get username
            fullname = instagram.getInformation.fullname(info) # You will get fullname
            follower = instagram.getInformation.follower_count(info)  # You will get follower count
            following = instagram.getInformation.following_count(info) # You will get following count
            media_count = instagram.getInformation.media_count(info)     # You will get media_count
            website_link = instagram.getInformation.external_url(info)    # You will get Website link
            is_private = instagram.getInformation.is_private(info)      # You will get is_private
            profilepic = instagram.getInformation.profile_hd_photo(info)  # You will get FullHd profile Image
            bio = instagram.getInformation.biography(info)         # You will get biography
            temp = pd.DataFrame(
                    {'userid': userid,
                     'username': username ,
                     'fullname': fullname,
                     'follower':follower,
                     'following':following,
                     'media_count':media_count,
                     'website_link' : website_link,
                     'is_private':is_private,
                     'profilepic':profilepic,
                     'bio':bio }, index=[0])
            d2 = pd.concat([d2, temp])
            print('end')
        except:
            continue
    return d2
    
    
    
d = pd.DataFrame()
shortcodes = get_pic_links()
total = len(shortcodes)
d = main(d,shortcodes,total)
d.to_csv('user-data.csv')


initial_data = pd.read_csv('/home/VIGNESHWAR.I/user-data.csv')



user_code = {k: g["Shortcode"].tolist() for k,g in initial_data.groupby("Listofusers")}

x = True
while x:
    user_data = pd.read_csv('/home/VIGNESHWAR.I/user-base1.csv')
    wehave = list(user_data['username'])
    userbase = list(set(initial_data['Listofusers']))
    if not wehave:
        x = False
    
    userbase2 = [i for i in userbase if i not in wehave]
    userbase2 = userbase2[:100]
    #d2 = pd.DataFrame()
    #d2 = get_user_details(userbase2,d2) 
    #
    user_data = get_user_details(userbase2,user_data) 
    user_data.to_csv('user-base1.csv')


#d2.to_csv('user-base1.csv')




########### 

#getting the number of likes from the dictionary
number_of_posts_liked = {}
for key, value in user_code.items():
    number_of_posts_liked[key] = len(value)

#adding new coumn to the user detail table to add the value and iterating and storing the value
user_data_copy = pd.read_csv('/home/VIGNESHWAR.I/user-base1.csv')
user_data_copy["likes_count"] = ""

for i, row in user_data_copy.iterrows():
    user_data_copy.set_value(i,'likes_count', number_of_posts_liked[row['username']])
    
    
    
    
    
##############To get datatime for every posts
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.instagram.com/p/'+'B0qTclJnCUY'+'/')
driver.execute_script("window.scrollTo(0, 1080)") 
python_button = driver.find_elements_by_xpath("//time[@class='_1o9PC Nzb55']")

