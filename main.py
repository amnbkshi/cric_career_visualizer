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




#fig = plt.figure()
fig, axes = plt.subplots(3, 2, sharex='col', sharey='row', figsize=(6,8))

axes[0, 0].bar(ODI_df.index,ODI_df['100'], width=0.5)
axes[0, 0].set_title('ODI', fontsize=16, fontweight="bold")
axes[0, 0].set_ylabel('Number of 100s', fontsize=10, fontweight="bold")

axes[0, 1].bar(test_df.index,test_df['100'], width=0.5, color='g')
axes[0, 1].set_title('Test', fontsize=16, fontweight="bold")

axes[1, 0].plot(ODI_df.index,ODI_df['Avg'], marker='o')
axes[1, 0].set_ylabel('Average', fontsize=10, fontweight="bold")

axes[1, 1].plot(test_df.index,test_df['Avg'], marker='o', color='g')

axes[2, 0].plot(ODI_df.index,ODI_df['SR'], marker='o')
axes[2, 0].set_ylabel('Strike Rate', fontsize=10, fontweight="bold")

axes[2, 1].plot(test_df.index,test_df['SR'], marker='o', color='g')


plt.savefig('sample.png')




















