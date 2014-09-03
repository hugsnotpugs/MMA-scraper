import pandas as pd
import numpy as np
import os
os.chdir('/Users/chuanhe/desktop/code')

df = pd.read_csv('FightMetric_Data_Master v2.csv')
df = df.drop_duplicates()
df['name'] = df.apply(lambda x: x['name_first'] + ' ' + x['name_last'], axis=1)
df['fight_id']= [i/2 if i%2 == 0 else (i-1)/2 for i in df.index]

bio_stats = pd.read_csv('Fighter_Stats_Master v2.csv')
bio_stats = bio_stats.drop_duplicates(cols=['name'])
bio_stats['age'] = bio_stats['age'].apply(lambda x: bio_stats['age'][bio_stats['age'] != 2014].median() if x == 2014 else x)


# Create a dictionary of unique fighters, with a corresponding list of their fight ids
fighter_dict = {}
for i in range(len(df['name'])):
    if df['name'][i] not in fighter_dict:
        fighter_dict[df['name'][i]] = [i]
    else:
        fighter_dict[df['name'][i]].append(i)

# Aggregate metrics
# Note: if you include head, leg, and body, you can linearly combine them to form sig_strike #
# Strikes is okay because it includes non-sig strikes which are not accounted for in location shots

fighter_df = pd.DataFrame(columns=['name', 'body', 'body_att', 'clinch', 'clinch_att', 'distance', 'distance_att',
                                   'ground', 'ground_att', 'head', 'head_att', 'leg', 'leg_att', 'method', 'pass', 
                                   'referee', 'reversal', 'round', 'sig_strike', 'sig_strike_att', 'strike', 'strike_att', 
                                   'sub', 'sub_att', 'td', 'td_att', 'win/loss', 'fight_id', 'fight_count', 'td_rec', 'td_rec_att',
                                   'head_rec', 'head_rec_att', 'sub_rec', 'sub_rec_att', 'strike_rec', 'strike_rec_att', 
                                   'sig_strike_rec', 'sig_strike_rec_att', 'clinch_rec', 'clinch_rec_att', 'ground_rec', 
                                   'ground_rec_att', 'body_rec', 'body_rec_att', 'leg_rec', 'leg_rec_att', 'total_rounds'])


# iterate through fighters such that...
for key in fighter_dict: 
    add_df = {'name': key}
    for column in fighter_df:
        if column != 'name':
            add_df[column] = 0
    
    count = 0
     # for each fighter, iterate backwards, from his earliest fight to most recent 
    for i in range(len(fighter_dict[key])-1, -1, -1):
        count += 1
        data_row = df.loc[fighter_dict[key][i]]
        
        if i-1 >= 0:
        	# i is the current fight, i+1 is the last fight, i-1 is the next fight
            result_row = df.loc[fighter_dict[key][i-1]] 
            add_df['win/loss'] = result_row['win/loss']
            add_df['fight_id'] = result_row['fight_id']
            add_df['referee'] = result_row['referee']
            add_df['round'] = result_row['round']
            add_df['total_rounds'] += result_row['round']
            add_df['method'] = result_row['method']
        else:
            add_df['win/loss'] = 2
            add_df['fight_id'] = 9999
            #add_df['fight_id'] 
            add_df['referee'] = 'None'
            add_df['round'] = 5
            add_df['total_rounds'] += 1
            add_df['method'] = 'None'

        # Find the opponent row
        if fighter_dict[key][i] < len(df)-1:
            if df.loc[fighter_dict[key][i]+1]['fight_id'] != data_row['fight_id']:
                opponent_row = df.loc[fighter_dict[key][i]-1]
            else:
                opponent_row = df.loc[fighter_dict[key][i]+1]
        else:
            opponent_row = df.loc[fighter_dict[key][i]-1]
            
        add_df['td_rec'] += opponent_row['takedowns']
        add_df['td_rec_att'] += opponent_row['td_attempts']
        add_df['head_rec'] += opponent_row['head']
        add_df['head_rec_att'] += opponent_row['head_attempts']
        add_df['sub_rec_att'] += opponent_row['sub_attempts']
        add_df['sig_strike_rec'] += opponent_row['sig_strikes']
        add_df['sig_strike_rec_att'] += opponent_row['sig_attempts']
        add_df['strike_rec'] += opponent_row['strikes']
        add_df['strike_rec_att'] += opponent_row['strike_attempts']
        add_df['clinch_rec'] += opponent_row['clinch']
        add_df['clinch_rec_att'] += opponent_row['clinch_attempts']
        add_df['ground_rec'] += opponent_row['ground']
        add_df['ground_rec_att'] += opponent_row['ground_attempts']
        add_df['head_rec'] += opponent_row['head']
        add_df['head_rec_att'] += opponent_row['head_attempts']
        add_df['body_rec'] += opponent_row['body']
        add_df['body_rec_att'] += opponent_row['body_attempts']
        add_df['leg_rec'] += opponent_row['leg']
        add_df['leg_rec_att'] += opponent_row['leg_attempts']
        
        if data_row['method'] == 'Submission' and data_row['win/loss'] == 1:
            add_df['sub'] += 1
        elif data_row['method'] == 'Submission' and data_row['win/loss'] == 0:
            add_df['sub_rec'] += 1
        
        add_df['body'] += data_row['body']
        add_df['body_att'] += data_row['body_attempts']
        add_df['clinch'] += data_row['clinch']
        add_df['clinch_att'] += data_row['clinch_attempts']
        add_df['distance'] += data_row['distance']
        add_df['distance_att'] += data_row['distance_attempts']
        add_df['ground'] += data_row['ground']
        add_df['ground_att'] += data_row['ground_attempts']
        add_df['head'] += data_row['head']
        add_df['head_att'] += data_row['head_attempts']
        add_df['leg'] += data_row['leg']
        add_df['leg_att'] += data_row['leg_attempts']
        add_df['pass'] += data_row['pass']
        add_df['reversal'] += data_row['reversals']
        add_df['sig_strike'] += data_row['sig_strikes']
        add_df['sig_strike_att'] += data_row['sig_attempts']
        add_df['strike'] += data_row['strikes']
        add_df['strike_att'] += data_row['strike_attempts']
        add_df['sub_att'] += data_row['sub_attempts']
        add_df['td'] += data_row['takedowns']
        add_df['td_att'] += data_row['td_attempts']            
        add_df['fight_count'] = count
        
        fighter_df = fighter_df.append(add_df, ignore_index=True)


# Define the variables that are not features
non_stats = ['name', 'win/loss', 'referee', 'round', 'method', 'fight_count', 'fight_id', 'distance_per', 'distance_%', 'pass_per',
             'reversal_per', 'total_rounds']

# Add the percentage and per fight columns
for column in fighter_df:
    if column not in non_stats:
        if column[-3:] == 'att':
            base = column[:-4]
            if column[-7:-4] == 'rec':
                fighter_df[column[:-7] + 'def_%'] = fighter_df.apply(lambda x: 0 if x[column] == 0 else x[base] / float(x[column]), axis=1)
            else:
                fighter_df[base + '_%'] = fighter_df.apply(lambda x: 1 if x[column] == 0 else 1 - (x[base] / float(x[column])), axis=1)
        else:
            fighter_df[column + '_per'] = fighter_df.apply(lambda x: x[column] / x['fight_count'], axis=1)
            
# Drop columns where necessary:
for column in fighter_df:
    if column not in non_stats:
        if column[-3:] != 'per' and column[-1:] != '%':
            fighter_df = fighter_df.drop(column, axis=1)


# Join fighter_df with the bio_df, drop null values and reset the index
fighter_df = fighter_df.merge(bio_stats, how='inner', on='name')
fighter_df = fighter_df.drop(labels=['win_%', 'referee'], axis=1)

fighter_df['reach'] = fighter_df['reach'].apply(lambda x: np.median(fighter_df['reach']) if pd.isnull(x) else x)
fighter_df['height'] = fighter_df['height'].apply(lambda x: np.median(fighter_df['height']) if pd.isnull(x) else x)
fighter_df = fighter_df.reset_index(drop=True)


# Create a dictionary of fights, with values as the fighters in each fight
fight_dict = {}
for i in range(len(fighter_df['fight_id'])):
    if fighter_df['fight_id'][i] not in fight_dict:
        fight_dict[fighter_df['fight_id'][i]] = [i]
    else:
        fight_dict[fighter_df['fight_id'][i]].append(i)


# Subtract each fighter's stats against their corresponding opponent's matching stats
# i.e., fighter1 Head Strikes vs. fighter2 Head Strikes defended
count = 0
for fight_key in fight_dict:
    if len(fight_dict[fight_key]) < 2:
        count += 1
    else:
        current = fighter_df.loc[fight_dict[fight_key][0]]
        opponent = fighter_df.loc[fight_dict[fight_key][1]]
        for column in current.index:
            if column not in non_stats:
                if column[-1:] == '%' and column[-3:] != 'f_%':
                    base_column = column[:-1]
                    temp_current = current[column] - opponent[base_column+'def_%']
                    temp_opponent = opponent[column] - current[base_column+'def_%']
                    fighter_df.loc[fight_dict[fight_key][0], column] = temp_current
                    fighter_df.loc[fight_dict[fight_key][1], column] = temp_opponent
                elif column[-5:] == 'def_%':
                    base_column = column[:-5]
                    temp_current = current[column] - opponent[base_column+'%']
                    temp_opponent = opponent[column] - current[base_column+'%']
                    fighter_df.loc[fight_dict[fight_key][0], column] = temp_current
                    fighter_df.loc[fight_dict[fight_key][1], column] = temp_opponent
                elif column[-3:] == 'per' and column[-5:] != 'c_per':
                    base_column = column[:-3]
                    temp_current = current[column] - opponent[base_column+'rec_per']
                    temp_opponent = opponent[column] - current[base_column+'rec_per']
                    fighter_df.loc[fight_dict[fight_key][0], column] = temp_current
                    fighter_df.loc[fight_dict[fight_key][1], column] = temp_opponent
                elif column[-7:] == 'rec_per':
                    base_column = column[:-7]
                    temp_current = current[column] - opponent[base_column+'per']
                    temp_opponent = opponent[column] - current[base_column+'per']
                    fighter_df.loc[fight_dict[fight_key][0], column] = temp_current
                    fighter_df.loc[fight_dict[fight_key][1], column] = temp_opponent
                elif column == 'age' or column == 'height' or column == 'reach':
                    temp_current = current[column] - opponent[column]
                    temp_opponent = opponent[column] - current[column]
                    fighter_df.loc[fight_dict[fight_key][0], column] = temp_current
                    fighter_df.loc[fight_dict[fight_key][1], column] = temp_opponent

fighter_df.to_csv('aggregated fightmetric stats.csv')
