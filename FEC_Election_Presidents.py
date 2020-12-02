# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 10:52:59 2020

@author: YTHAKUR
"""

import pandas as pd 
import numpy as np
pd.set_option(r'display.max_columns', None)

cdm_2018 = pd.read_csv(r'CandiMas_18.txt', sep = '|', low_memory = False, header = None)
cdm_2018['CandidateID'] = cdm_2018[0]
cdm_2018['Name'] = cdm_2018[1]
cdm_2018['Political Party Affiliation'] = cdm_2018[2]
cdm_2018['Year of Election'] = cdm_2018[3]
cdm_2018['Office'] = cdm_2018[5]
cdm_2018['Principal Campaign Committee'] = cdm_2018[9]
cdm_2018 = cdm_2018.drop([i for i in range(0,15)],1)
cdm_2018 = cdm_2018[cdm_2018['Office'] == 'P'].reset_index()
cdm_2018 = cdm_2018.drop('index',1)

ac_2018 = pd.read_csv(r'CandiALL_18.txt', sep = '|', low_memory= False, header = None)
ac_2018['CandidateID'] = ac_2018[0]
ac_2018['Total Receipts'] = ac_2018[5]
ac_2018['Total Disbursements'] = ac_2018[7]
ac_2018 = ac_2018.drop([i for i in range(0,30)],1)
c18_cdm_ac = pd.merge(cdm_2018, ac_2018, on = 'CandidateID', how = 'left')

cc_2018 = pd.read_csv(r'Candi_comm_18.txt', sep = '|', low_memory= False, header = None)
cc_2018['CandidateID'] = cc_2018[0]
cc_2018['CommitteeID2'] = cc_2018[3]
cc_2018 = cc_2018.drop([i for i in range(0,7)],1)
cc_2018 = cc_2018[cc_2018['CandidateID'].str.startswith('P')]
c18_cdm_ac_cc = pd.merge(c18_cdm_ac, cc_2018, on = 'CandidateID', how = 'left')
for i in range(len(c18_cdm_ac_cc['CandidateID'])):
    if c18_cdm_ac_cc['Principal Campaign Committee'][i] is np.nan: c18_cdm_ac_cc['CommitteeID'] = c18_cdm_ac_cc['CommitteeID2']
    else: 
        if c18_cdm_ac_cc['CommitteeID2'][i] is np.nan: c18_cdm_ac_cc['CommitteeID'] = c18_cdm_ac_cc['CommitteeID2']
        else: c18_cdm_ac_cc['CommitteeID'] = c18_cdm_ac_cc['Principal Campaign Committee'] 
c18_cdm_ac_cc = c18_cdm_ac_cc.drop(['CommitteeID2', 'Principal Campaign Committee'],1)

opex_2018 = pd.read_csv(r'OPEX_18.txt', sep = "|", low_memory=False, header = None)
opex_2018['CommitteeID'] = opex_2018[0]
opex_2018['TRANSACTION_DT'] = opex_2018[12]
opex_2018['TRANSACTION_AMNT'] = opex_2018[13]
opex_2018['TRANSACTION_PGI'] = opex_2018[14]
opex_2018['PURPOSE'] = opex_2018[15].str.lower()
opex_2018['CATEGORY'] = opex_2018[16]
opex_2018['CATEGORY_DESC'] = opex_2018[17]
opex_2018 = opex_2018.drop([i for i in range(0,25)],1)
opex_2018['TCDIS'] = pd.np.where(opex_2018.PURPOSE.str.contains('distribute' or 'advertise' or 'advertising' or 'advertisement' or 'buy' or 'ad' or 'placement' or 'target'),'nonCLassified_AD',
                                          pd.np.where(opex_2018.PURPOSE.str.contains('direct' or 'page' or 'market' or 'endors'),'nonCLassified_AD_doubt',
                                          pd.np.where(opex_2018.PURPOSE.str.contains('digit' or 'online' or 'website' or 'google' or 'internet' or 'web'),'digital',
                                          pd.np.where(opex_2018.PURPOSE.str.contains('radio' or 'time' or 'tv' or 'televise' or 'television'),'broadcast',
                                          pd.np.where(opex_2018.PURPOSE.str.contains('print' or 'literature' or 'press' or 'line' or 'release' or 'magazine' or 'newspaper' or 'printing'),'Print',
                                          pd.np.where(opex_2018.PURPOSE.str.contains('email' or 'e-mail'),'email',
                                          pd.np.where(opex_2018.PURPOSE.str.contains('media'),'media',
                                          pd.np.where(opex_2018.PURPOSE.str.contains('social' or 'twitter' or 'facebook' or 'social' or 'youtube' or 'blog'),'socialMedia',
                                          pd.np.where(opex_2018.PURPOSE.str.contains('mail' or 'mailer' or 'postcard' or 'postage' or 'stamp' or 'post' or 'envelope' or 'mailhouse'),'directMail',
                                          pd.np.where(opex_2018.PURPOSE.str.contains('billboard' or 'banner' or 'sign' or 'signs' or 'poster' or 'flyer' or 'week' or 'dissemin' or 'filer'),'posters', "Unclassified"))))))))))
opex_18_consolidated = opex_2018.groupby(['CommitteeID', 'TCDIS'])['TRANSACTION_AMNT'].sum().reset_index()
opex_18 = opex_18_consolidated.pivot_table(values='TRANSACTION_AMNT', index = 'CommitteeID', columns='TCDIS', aggfunc = 'first')
opex_18['digitalMedia'] = opex_18.apply(lambda row: row.digital + row.email + row.socialMedia , axis=1)
opex_18['nonDigitalMedia'] = opex_18.apply(lambda row: row.posters + row.broadcast + row.nonCLassified_AD + row.nonCLassified_AD_doubt + row.Print , axis=1)
opex_18['totalMedia'] = opex_18.apply(lambda row: row.digitalMedia + row.nonDigitalMedia + row.media, axis=1)
opex_18['totalADSpending'] = opex_18.apply(lambda row: row.totalMedia + row.directMail, axis=1)
c18_cdm_ac_cc_opex = pd.merge(c18_cdm_ac_cc, opex_18, on = 'CommitteeID', how = 'left').fillna(0)
c18_cdm_ac_cc_opex.to_csv('FEC_Presidents_2018.csv', index=False)