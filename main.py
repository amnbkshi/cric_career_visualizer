#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 14:20:19 2019

@author: aman
"""

import bs4
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver

plt.style.use('seaborn-darkgrid')

URL = "http://www.cricmetric.com/playerstats.py?player=V%20Kohli"

def html_to_df(table):
    
    rows = []
    
    for row in table.find_all('tr'):
        column = []
        for col in row.find_all(['th', 'td']):
            column.append(col.text)
        rows.append(column)
        
    df = pd.DataFrame(rows[1:-2], columns=rows[0])    
    df.set_index('Year', inplace=True)
    
    for col in df:
        try:
            df[col] = df[col].str.replace(',', '').astype(float)
        except ValueError:
            pass
    
    return df

options = webdriver.FirefoxOptions()
options.headless = True
browser = webdriver.Firefox(options=options)

browser.get(URL)

html = browser.page_source
soup = bs4.BeautifulSoup(html, "html.parser")


element1 = soup.find('div', {"id":"Test-Batting"})
test_table = element1.find('table')

element2 = soup.find('div', {"id":"ODI-Batting"})
ODI_table = element2.find('table')

test_df = html_to_df(test_table)
ODI_df = html_to_df(ODI_table)




fig = plt.figure()
#
#plt.subplot(3, 2, 1)
#plt.plot(ODI_df.index,ODI_df['100'], marker='o')
#
#plt.subplot(3, 2, 2)
#plt.plot(test_df.index,test_df['100'], marker='o')
#
#plt.subplot(3, 2, 3)
#plt.plot(ODI_df.index,ODI_df['Avg'], marker='o')
#
#plt.subplot(3, 2, 4)
#plt.plot(test_df.index,test_df['Avg'], marker='o')
#
#plt.subplot(3, 2, 5)
#plt.plot(ODI_df.index,ODI_df['SR'], marker='o')
#
#plt.subplot(3, 2, 6)
#plt.plot(test_df.index,test_df['SR'], marker='o')

plt.subplot(3, 2, 1)
plt.bar(ODI_df.index,ODI_df['100'])
plt.title('ODI')
plt.ylabel('Number of 100s')

plt.subplot(3, 2, 2)
plt.bar(test_df.index,test_df['100'])
plt.title('Test')

plt.subplot(3, 2, 3)
plt.plot(ODI_df.index,ODI_df['Avg'], marker='o')
plt.ylabel('Average')

plt.subplot(3, 2, 4)
plt.plot(test_df.index,test_df['Avg'], marker='o')

plt.subplot(3, 2, 5)
plt.plot(ODI_df.index,ODI_df['SR'], marker='o')
plt.ylabel('Strike Rate')

plt.subplot(3, 2, 6)
plt.plot(test_df.index,test_df['SR'], marker='o')






















