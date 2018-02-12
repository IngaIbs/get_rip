#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

DEATH SCRAPER 0.1 alpha

"""

import requests



def get_name(text,idx):
    search = ["searchTitle",">"," "]
    
    for pattern in search:
        idx = text.find(pattern,idx)
        
        if(idx==-1):
            return "",-1
                        
    name = text[idx:text.find("<",idx)]
        
    return name,idx


def get_dates(text,idx):
    idx = text.find("labelSearchItem",idx) + 17
    stop_idx = text.find("<",idx)
    
    if(idx==stop_idx):
        return 0,0

    if(text[idx] == "*"):
        birth_date = text[idx+2:text.find(" ",idx+2)]
    else:
        birth_date = 0
        
    death_date = text[text.find("; ",idx)+2:stop_idx]
    
    
    return birth_date,death_date


url = 'https://trauer.tagesspiegel.de/traueranzeigen/_/_/_/0/0/'


page_count = 20

not_done = True
for page_idx in range(page_count):

    text = requests.get(url + str(page_idx)).text


    idx = 0
    while(not_done):
        
        name,idx = get_name(text,idx)
        
        if(idx==-1):
            break
    
        b,d = get_dates(text,idx)
        
        
        print(name,b,d)
