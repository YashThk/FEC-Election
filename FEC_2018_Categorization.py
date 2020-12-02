# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 11:16:16 2020

@author: YashThk
"""

import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

opex_2018 = pd.read_csv(r'C:\Users\HP\OPEX_2018.txt', sep = "|", low_memory=False, header = None)

opex_2018['CMTE_ID'] = opex_2018[0]
opex_2018['AMNDT_ID'] = opex_2018[1]
opex_2018['RPT_YR'] = opex_2018[2]
opex_2018['RPT_TP'] = opex_2018[3]
opex_2018['IMAGE_NUM'] = opex_2018[4]
opex_2018['LINE_NUM'] = opex_2018[5]
opex_2018['FORM_TP_CD'] = opex_2018[6]
opex_2018['SCHED_TP_CD'] = opex_2018[7]
opex_2018['NAME'] = opex_2018[8]
opex_2018['CITY'] = opex_2018[9]
opex_2018['STATE'] = opex_2018[10]
opex_2018['ZIP_CODE'] = opex_2018[11]
opex_2018['TRANSACTION_DT'] = opex_2018[12]
opex_2018['TRANSACTION_AMNT'] = opex_2018[13]
opex_2018['TRANSACTION_PGI'] = opex_2018[14]
opex_2018['PURPOSE'] = opex_2018[15].str.lower()
opex_2018['CATEGORY'] = opex_2018[16]
opex_2018['CATEGORY_DESC'] = opex_2018[17]
opex_2018['MEMO_CD'] = opex_2018[18]
opex_2018['MEMO_TEXT'] = opex_2018[19]
opex_2018['ENTITY_TP'] = opex_2018[20]
opex_2018['SUB_ID'] = opex_2018[21]
opex_2018['FILE_NUM'] = opex_2018[22]
opex_2018['TRANSACTION_ID'] = opex_2018[23]
opex_2018['BACK_REF_TRAN_ID'] = opex_2018[24]
opex_2018 = opex_2018.drop(opex_2018.columns[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]], axis=1)
opex_2018.reset_index(inplace=True)
opex_2018 = opex_2018.rename(columns = {'index':'ID'})

houseElection_2018 = pd.read_csv(r'C:\Users\HP\2018 House Elections 11-08.csv', low_memory=False, encoding='cp1252')

houseElection_2018_positive1 = []
houseElection_2018_negative = []

for j in range(len(houseElection_2018['candidate_id'])):
    if houseElection_2018['Flag'][j] == 1:
        houseElection_2018_negative.append(houseElection_2018['committee_id'][j])
    else:
        houseElection_2018_positive1.append(houseElection_2018['committee_id'][j])
 
houseElection_2018_positive = [x for x in houseElection_2018_positive1 if str(x) != 'nan']

is_negative = opex_2018['CMTE_ID'].isin(houseElection_2018_negative)
is_positive = opex_2018['CMTE_ID'].isin(houseElection_2018_positive)
opex_2018_negative = opex_2018[is_negative].reset_index()
opex_2018_positive = opex_2018[is_positive].reset_index()
opex_2018_negative['TCDIS'] = pd.np.where(opex_2018_negative.PURPOSE.str.contains('distribute' or 'advertise' or 'advertising' or 'advertisement' or 'buy' or 'ad' or 'placement' or 'target'),'nonCLassified_AD',
                                          pd.np.where(opex_2018_negative.PURPOSE.str.contains('direct' or 'page' or 'market' or 'endors'),'nonCLassified_AD_doubt',
                                          pd.np.where(opex_2018_negative.PURPOSE.str.contains('digit' or 'online' or 'website' or 'google' or 'internet' or 'web'),'digital',
                                          pd.np.where(opex_2018_negative.PURPOSE.str.contains('radio' or 'time' or 'tv' or 'televise' or 'television'),'broadcast',
                                          pd.np.where(opex_2018_negative.PURPOSE.str.contains('print' or 'literature' or 'press' or 'line' or 'release' or 'magazine' or 'newspaper' or 'printing'),'Print',
                                          pd.np.where(opex_2018_negative.PURPOSE.str.contains('email' or 'e-mail'),'email',
                                          pd.np.where(opex_2018_negative.PURPOSE.str.contains('media'),'media',
                                          pd.np.where(opex_2018_negative.PURPOSE.str.contains('social' or 'twitter' or 'facebook' or 'social' or 'youtube' or 'blog'),'socialMedia',
                                          pd.np.where(opex_2018_negative.PURPOSE.str.contains('mail' or 'mailer' or 'postcard' or 'postage' or 'stamp' or 'post' or 'envelope' or 'mailhouse'),'directMail',
                                          pd.np.where(opex_2018_negative.PURPOSE.str.contains('billboard' or 'banner' or 'sign' or 'signs' or 'poster' or 'flyer' or 'week' or 'dissemin' or 'filer'),'posters', "Unclassified"))))))))))
opex_2018_positive['TCDIS'] = pd.np.where(opex_2018_positive.PURPOSE.str.contains('distribute' or 'advertise' or 'advertising' or 'advertisement' or 'buy' or 'ad' or 'placement' or 'target'),'nonCLassified_AD',
                                          pd.np.where(opex_2018_positive.PURPOSE.str.contains('direct' or 'page' or 'market' or 'endors'),'nonCLassified_AD_doubt',
                                          pd.np.where(opex_2018_positive.PURPOSE.str.contains('digit' or 'online' or 'website' or 'google' or 'internet' or 'web'),'digital',
                                          pd.np.where(opex_2018_positive.PURPOSE.str.contains('radio' or 'time' or 'tv' or 'televise' or 'television'),'broadcast',
                                          pd.np.where(opex_2018_positive.PURPOSE.str.contains('print' or 'literature' or 'press' or 'line' or 'release' or 'magazine' or 'newspaper' or 'printing'),'Print',
                                          pd.np.where(opex_2018_positive.PURPOSE.str.contains('email' or 'e-mail'),'email',
                                          pd.np.where(opex_2018_positive.PURPOSE.str.contains('social' or 'twitter' or 'facebook' or 'social' or 'youtube' or 'blog'),'socialMedia',
                                          pd.np.where(opex_2018_positive.PURPOSE.str.contains('mail' or 'mailer' or 'postcard' or 'postage' or 'stamp' or 'post' or 'envelope' or 'mailhouse'),'directMail',
                                          pd.np.where(opex_2018_positive.PURPOSE.str.contains('billboard' or 'banner' or 'sign' or 'signs' or 'poster' or 'flyer' or 'week' or 'dissemin' or 'filer'),'posters', "Unclassified")))))))))

opex_2018_negative_consolidated = opex_2018_negative.groupby(['CMTE_ID', 'TCDIS'])['TRANSACTION_AMNT'].sum().reset_index()
opex_2018_positive_consolidated = opex_2018_positive.groupby(['CMTE_ID', 'TCDIS'])['TRANSACTION_AMNT'].sum().reset_index()

negative_df = opex_2018_negative_consolidated.pivot_table(values='TRANSACTION_AMNT', index = 'CMTE_ID', columns='TCDIS', aggfunc = 'first')
positive_df = opex_2018_positive_consolidated.pivot_table(values='TRANSACTION_AMNT', index = 'CMTE_ID', columns='TCDIS', aggfunc = 'first')

negative_df = negative_df.fillna(0)
positive_df = positive_df.fillna(0)

negative_df['digitalMedia'] = negative_df.apply(lambda row: row.digital + row.email + row.socialMedia , axis=1)
negative_df['nonDigitalMedia'] = negative_df.apply(lambda row: row.posters + row.broadcast + row.nonCLassified_AD + row.nonCLassified_AD_doubt + row.Print , axis=1)
negative_df['totalMedia'] = negative_df.apply(lambda row: row.digitalMedia + row.nonDigitalMedia + row.media, axis=1)
negative_df['totalADSpending'] = negative_df.apply(lambda row: row.totalMedia + row.directMail, axis=1)

positive_df['digitalMedia'] = positive_df.apply(lambda row: row.digital + row.email + row.socialMedia , axis=1)
positive_df['nonDigitalMedia'] = positive_df.apply(lambda row: row.posters + row.broadcast + row.nonCLassified_AD + row.nonCLassified_AD_doubt + row.Print , axis=1)
positive_df['totalMedia'] = positive_df.apply(lambda row: row.digitalMedia + row.nonDigitalMedia, axis=1)
positive_df['totalADSpending'] = positive_df.apply(lambda row: row.totalMedia + row.directMail, axis=1)


negative_df.to_csv('negative_df.csv', index=True)
positive_df.to_csv('positive_df.csv', index=True)

#opex_2018_negative.to_csv('OPEX_2018_N.csv', index=False)
#opex_2018_negative_consolidated.to_csv('OPEX_2018_NC.csv', index=False)
#opex_2018_positive.to_csv('OPEX_2018_P.csv', index=False)
#opex_2018_positive_consolidated.to_csv('OPEX_2018_PC.csv', index=False)