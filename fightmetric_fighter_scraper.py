from bs4 import BeautifulSoup
import pandas as pd
import urllib
import os
os.chdir('/Users/chuanhe/desktop/code')

# Load URLs from CSV (created in fightmetric_scraper.py)
fighter_urls = pd.read_csv('fighter urls.csv', encoding='utf-8')

# Initialize an empty dataframe
fighter_bio_df = pd.DataFrame(columns=['name', 'height', 'reach', 'age', 'win_%'])

# Iterate through fighter_urls and pull relevant information
for i in range(len(fighter_urls)):
    fighter_bio_dict = {}
    name_dict = {}
    sock = urllib.urlopen(fighter_urls[i]) # specific URL for a fight
    fight_html = sock.read()
    fight_soup = BeautifulSoup(fight_html)
    headers = fight_soup.find_all('li')
    names = fight_soup.find_all('span')
    bad_call = 0
    
    try: 
        year = int(str(headers[13].get_text()).split()[-1])
    except:
        year = 0
        bad_call +=1
        print str(i) + ' bad call' if i%50 == 0 else None
    try:
        reach = float(str(headers[11].get_text()).split()[1][:2])
    except:
        reach = None
        bad_call +=1
        print str(i) + ' bad call' if i%50 == 0 else None
    try:
        height = float(str(headers[9].get_text()).split()[1][0]) + float(str(headers[9].get_text()).split()[2][:-1])/12
    except:
        height = None
        bad_call +=1
        print str(i) + ' bad call' if i%50 == 0 else None
    try:
        win = float(str(names[1].get_text()).split()[1].split('-')[0]) / (float(str(names[1].get_text()).split()[1].split('-')[0]) + float(str(names[1].get_text()).split()[1].split('-')[1]))
    except:
        win = 0
        bad_call +=1
        print str(i) + ' bad call' if i%50 == 0 else None
    try: 
        name = str(names[0].get_text()).split()[0] + ' ' + str(names[0].get_text()).split()[1]
    except:
        name = None
        bad_call +=1
        print str(i) + ' bad call' if i%50 == 0 else None
        
    
    fighter_bio_dict = {'name': name, 'height': height, 'reach': reach, 'age': 2014 - year, 'win_%': win}
    
    # Add dictionary information to the dataframe
    if name not in name_dict:
        name_dict[name] = 0
        fighter_bio_df = fighter_bio_df.append(fighter_bio_dict, ignore_index=True)
