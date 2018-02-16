#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Search for Death Notices on Newspaper Websites
"""


from bs4 import BeautifulSoup
import requests


file = open("LinksZeitungen.txt")

Links = []

for line in file:
    Links.append(line)

file.close()

Links = [link[1:] for link in Links[0].split(">")]

#%%

DirectLinks = []

Cities = []

for link in Links:
    if(link != ''):
        url,Stadt = link.split(";")
        DirectLinks.append(url)
        Cities.append(Stadt)
        
        
#%%
        
TrauerLinks  = {}

for i,url in enumerate(DirectLinks):
    print(i,"/",len(DirectLinks))
    
    try:
        r = requests.get(url)
    except:
        pass
    else:
        
        soup = BeautifulSoup(r.text,"lxml")
        
        if(not TrauerLinks.__contains__(Cities[i])):
            TrauerLinks[Cities[i]] = []
            
        for Pot in soup.findAll("a"):
            if(len(Pot.contents) > 0 and "Trauer" in Pot.contents[0]):
                
                LinkT = Pot["href"]
                
                if(LinkT[0]=='/'):
                    if(url[-1] == '/'):
                        LinkT = url+LinkT[1:]
                    else:
                        LinkT = url + LinkT
                
                if(not LinkT in TrauerLinks[Cities[i]]):
                    TrauerLinks[Cities[i]].append(LinkT)
                    
                

#%%
import csv
                    
with open("TrauerPortale.csv",'w') as resultFile:
    wr = csv.writer(resultFile)
    
    for City in TrauerLinks:
        if(len(TrauerLinks[City])>0):
            wr.writerow([City] + TrauerLinks[City])








