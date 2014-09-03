from bs4 import BeautifulSoup
import pandas as pd
import urllib
import os
os.chdir('/Users/chuanhe/desktop/code')

# Load URLs from CSV (created in fightmetric_scraper.py)
fight_urls = pd.read_csv('fight urls.csv', encoding='utf-8')

# Initialize an empty dataframe
fighter_df = pd.DataFrame(columns=['name_first', 'name_last', 'kd', 'sig_strikes', 'sig_attempts', 'strikes', 'strike_attempts', 
                                   'takedowns', 'td_attempts', 'sub_attempts', 'pass', 'reversals', 'head', 'head_attempts', 'body', 
                                   'body_attempts','leg', 'leg_attempts', 'distance', 'distance_attempts', 'clinch', 'fight_id',
                                   'clinch_attempts', 'ground', 'ground_attempts', 'win/loss', 'referee', 'round', 'method'])


# Iterate through the fight urls, and pull relevant variables/fields
for i in range(len(fight_urls)):
    print fight_urls[i]
    
    sock = urllib.urlopen(fight_urls[i]) # specific URL for a fight
    fight_html = sock.read()
    fight_soup = BeautifulSoup(fight_html)
    trs = fight_soup.find_all('tr') # all the tables in each fight URL
    headers = fight_soup.find_all('i')
    bad_call = 0
    try: 
        referee = str(headers[24].get_text()).split()[1] + ' ' + str(headers[24].get_text()).split()[-1]
    except:
        referee = None
    try:
        rounds = str(headers[18].get_text()).split()[1]
    except:
        rounds = None
    try:
        method = str(headers[17].get_text()).split()[0]
    except:
        method = None
    try:
        tr1 = str(trs[1].get_text()).split()
        # Find the location of the 2nd table tr2 (it varies)
        j = 0
        while j < 10:
            if str(trs[j].get_text()).split()[6] == 'Head':
                #print j+1
                tr2 = str(trs[j+1].get_text()).split()
                j = 10
            else:
                j += 1
        #print tr1; #print tr2
        
        # Test for the end of names
        k = 0
        while k < len(tr1):
            try:
                int(tr1[k])
                break
            except:
                k += 1
                continue
        #print k
    except:
        print str(i) + ' bad call' if i%20 == 0 else None
        bad_call += 1
        continue


    # Add each fighter's information to the dataframe
    fighter1 = pd.DataFrame({'name_first': tr1[:1], 'name_last': tr1[1:2], 'kd': tr1[k], 'sig_strikes': tr1[k+2],
    'sig_attempts': tr1[k+4], 'strikes': tr1[k+10], 'strike_attempts': tr1[k+12], 'takedowns': tr1[k+16],'td_attempts': tr1[k+18],
    'sub_attempts': tr1[k+24], 'pass': tr1[k+26], 'reversals': tr1[k+28], 'head': tr2[k+8], 'head_attempts': tr2[k+10],
    'body': tr2[k+14], 'body_attempts': tr2[k+16], 'leg': tr2[k+20], 'leg_attempts': tr2[k+22], 'distance': tr2[k+26],
    'distance_attempts': tr2[k+28], 'clinch': tr2[k+32], 'clinch_attempts': tr2[k+34], 'ground': tr2[k+38], 
    'ground_attempts': tr2[k+40], 'win/loss': 1, 'referee': referee, 'round': rounds, 'method': method, 'fight_id': i})

    fighter2 = pd.DataFrame({'name_first': tr1[2:3], 'name_last': tr1[3:4], 'kd': tr1[k+1], 'sig_strikes': tr1[k+5], 
    'sig_attempts': tr1[k+7], 'strikes': tr1[k+13], 'strike_attempts': tr1[k+15], 'takedowns': tr1[k+19],'td_attempts': tr1[k+21],
    'sub_attempts': tr1[k+25], 'pass': tr1[k+27], 'reversals': tr1[k+29], 'head': tr2[k+11], 'head_attempts': tr2[k+13],
    'body': tr2[k+17], 'body_attempts': tr2[k+19], 'leg': tr2[k+23], 'leg_attempts': tr2[k+25], 'distance': tr2[k+29],
    'distance_attempts': tr2[k+31], 'clinch': tr2[k+35], 'clinch_attempts': tr2[k+37], 'ground': tr2[k+41], 
    'ground_attempts': tr2[k+43], 'win/loss': 0, 'referee': referee, 'round': rounds, 'method': method, 'fight_id': i})
    
    fighter_df = pd.concat([fighter_df, fighter1, fighter2], axis=0, ignore_index=True)
    
