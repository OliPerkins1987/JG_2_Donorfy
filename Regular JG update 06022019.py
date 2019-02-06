# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:03:47 2018

@author: Oli
"""



import pandas as pd
import numpy as np
import os
from copy import deepcopy


############################################################
# import data
############################################################


### 1. Load JG Donation report

os.chdir(r'C:\Users\Oli\Documents\Reverserett\Locker\Donorfy\Regular updates\JG Donations\4 October 2018')

data_2018                         = pd.read_csv('DonationsReport-CharityId-189388-from-2018-01-01-to-2018-11-04.csv')
data_2018['Donation Date']        = pd.to_datetime(data_2018['Donation Date'])
data_2018                         = data_2018[data_2018['Donation Date'] > '21/09/2018']
np.min(data_2018['Donation Date'])


### 2. Load donorfy

os.chdir(r'C:\Users\Oli\Documents\Reverserett\Locker\Donorfy\Regular updates\JG Donations\6 November')

Donorfy                           = pd.read_csv('download_all_constituents_download_2018-11-06_16-30-01.csv')


### 3. Load templates

Constituents                      = pd.read_excel('Constituent Template.xlsx')
Donations                         = pd.read_excel('Donation Template.xlsx')

'''

1. Isolate Constituents already in donorfy from new donors

'''

data_Donorfy                      = data_2018[data_2018['Donor User Id'].isin(Donorfy['Constituent_ExternalKey'])]
data_new                          = data_2018[data_2018['Donor User Id'].isin(data_Donorfy['Donor User Id']) == False]

### filter new data for is further contact == True

data_new                          = data_new[data_new['Donor Further Contact'] == 'Yes']


'''

2.Move data into upload templates

'''

#### 2.1 Donation Data


def transfer_donations(source, template):
    ''' takes a financial donorfy excel template and moves JG report data over to it.'''
    ''' The JG data should be a report with all available columns in it '''
    
    x                   = deepcopy(template)
    x['ExternalKey']    = source['Donor User Id']
    x['Amount']         = source['Donation Auth Amount']
    x['Date Paid']      = source['Donation Date']
    x['Campaign']       = np.select([source['Appeal Name'] == 'General Appeal', source['Appeal Name'] != 'General Appeal'], ['General Campaign', 'Reverse MECP2'])
    x['Fund']           = np.select([source['Appeal Name'] == 'General Appeal', source['Appeal Name'] != 'General Appeal'], ['General', 'MeCP2 Duplication Fund'])
    x['Processing Costs'] = [0.05*x for x in source['Donation Auth Amount'].tolist()]
    x['Payment Method'] = 'JustGiving'
    x['Product']        = 'Donation'
    x['Exclude from Gift Aid Claim'] = 'Yes'
    
    return(x)

def varname( var, dir=locals()):
    return [ key for key, val in dir.items() if id( val) == id( var)]

def write_out(file):
    os.chdir(r'C:\Users\Oli\Documents\Reverserett\Locker\Donorfy\Regular updates\JG Donations\6 November')
    os.mkdir(str(varname(file)))
    os.chdir(str(varname(file)))
    filename = varname(file)
    filename = str(filename) + '.xlsx'
    file.to_excel(str(filename), index = False, sheet_name = 'Donations')

# Process

Newdons_Donorfy    = transfer_donations(data_Donorfy, Donations)
write_out(Newdons_Donorfy)

Newdons_notDonorfy = transfer_donations(data_new, Donations)
write_out(Newdons_notDonorfy)



### 2.2 Constituent Data

data_cons = data_new[(data_new.duplicated(subset = 'Donor User Id', keep = 'first') == False)]

def write_out_cons(file):
    os.chdir(r'C:\Users\Oli\Documents\Reverserett\Locker\Donorfy\Regular updates\JG Donations\6 November')
    os.mkdir(str(varname(file)))
    os.chdir(str(varname(file)))
    filename = varname(file)
    filename = str(filename) + '.xlsx'
    file.to_excel(str(filename), index = False, sheet_name = 'Individual Constituents')


def transfer_constituents(source, template):
    ''' takes a constituent donorfy excel template and moves JG report data over to it.'''
    ''' The JG data should be a report with all available columns in it '''

    x                   = deepcopy(template)
   
    x['Block_Email']    = 'No'    
    x['Personal_AddressLine1'] = source['Donor Address Line 1']
    x['Personal_AddressLine2'] = source['Donor Address Line 2']
    x['Personal_Town'] = source['Donor Town']
    x['Personal_PostalCode'] = source['Donor Postcode']
    x['Personal_County'] = source['Donor County']
    x['Personal_Email1Address'] = source['Donor E-mail']
    x['FirstName']      = source['Donor FirstName']
    x['LastName']       = source['Donor LastName']
    x['ExternalKey']    = source['Donor User Id']   
    x['Allow_Purpose_E-newsletter']     = 'Yes'
    x['Allow_Purpose_Events - general'] = 'Yes'
    x['Allow_Purpose_Events - London']  = 'Yes'
    x['Allow_Purpose_Events - North Berwick'] = 'Yes'
    x['Tag_Data Source_Just Giving post April 2018'] = 'Yes'
    x['Tag_Segment Tags_4M'] = 'Yes'
    
    return(x)

New_Constituents = transfer_constituents(data_cons, Constituents)
write_out_cons(New_Constituents)
















