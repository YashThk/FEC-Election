"""
Created on Fri Oct  9 17:06:53 2020

@author: YashThk
"""

import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

opex_2018 = pd.read_csv(r'C:\Users\HP\OPEX_2018.txt', sep = "|", low_memory=False, header = None)

houseElection_2018 = pd.read_csv(r'C:\Users\HP\2018 House Elections 11-08.csv', low_memory=False, encoding='cp1252')

houseEelction_2018_edit = houseElection_2018[houseElection_2018['Flag'] == 1]
#houseEelction_2018_edit = houseElection_2018[houseElection_2018['Flag'] == 0]     Uncomment for disbursements less than expenditure


list_comt_id = houseEelction_2018_edit['committee_id'].tolist()

opex_2018 = opex_2018[opex_2018[0].isin(list_comt_id)]

opex_2018 = opex_2018.drop(opex_2018.columns[[1,2,3,4,5,6,7,8,9,10,11,12,14,18,19,20,21,22,24,25]], axis=1)
 

opex_2018['CMTE_ID'] = opex_2018[0]
opex_2018['TRANSACTION_AMNT'] = opex_2018[13]
opex_2018['CATEGORY'] = opex_2018[16]
opex_2018['CATEGORY_DESC'] = opex_2018[17]
opex_2018['PURPOSE'] = opex_2018[15]
opex_2018['TRANSACTION_ID'] = opex_2018[23]

opex_2018 = opex_2018.drop(opex_2018.columns[[0,1,2,3,4,5]], axis=1)
       
opex_2018.groupby(['CMTE_ID'])['PURPOSE']

df_pupose_unique =  opex_2018.groupby(['PURPOSE', 'CATEGORY', 'CATEGORY_DESC'])['TRANSACTION_AMNT'].sum().reset_index()
df_pupose_unique.to_csv('PURPOSE_UNIQUE_NEGETIVE.csv', index = False)
#df_pupose_unique.to_csv('PURPOSE_UNIQUE_POSITIVE.csv', index = False)              Uncomment for disbursements less than expenditure



