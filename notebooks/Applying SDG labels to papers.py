#!/usr/bin/env python
# coding: utf-8

# # Applying SDG labels to publications
# 
# This script makes use of the Open SDG proejct (https://osdg.ai/) and (https://github.com/osdg-ai/osdg-tool/tree/pre-release) to determine which SDG labels should be applied to publications based on the title + abstract. 
# 
# 
# 

# In[1]:


import requests
import pandas as pd


# In[2]:


osdg_url = 'http://docker-dev.vliz.be:5001/tag'
data_file = 'lifewatch_pubs_20211004.xlsx'


# In[3]:


def get_sdg(row):
    text = str(row['StandardTitle']) + str(row['AbstractEnglish'])
    text_dict = {'text':text}
    try:
        response = requests.post(osdg_url, json=text_dict)
        result = response.json()
        row['result_status'] = result['status']
        row['result'] = {item['sdg']:item['relevance'] for item in result['result']}  
    except Exception as err:
        print('Something went wrong')
        row['result_status'] = 'nOK'
        row['result'] = [err]
    return row


# In[4]:


df = pd.read_excel(data_file)


# In[5]:


# Reduce number of rows with duplicate titles and abstract
df = df.drop_duplicates(subset=['StandardTitle', 'AbstractEnglish'])
small_df = df.iloc[1000:1100]


# In[8]:


small_df  = small_df.apply(lambda row: get_sdg(row), axis=1)
small_df


# ## Sorta Pivot to get the dict info into columns...
# Currently the SDG labels are stored in a dict with the SDG# and relevance value. It would be better to have a bunch of columns with the values in there.
# 
# https://stackoverflow.com/questions/38231591/split-explode-a-column-of-dictionaries-into-separate-columns-with-pandas

# In[7]:


small_df.join(small_df['result'].apply(pd.Series))

