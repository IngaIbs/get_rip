#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOBFS TrauerTaucher
"""

from bs4 import BeautifulSoup
import mechanicalsoup
import requests


def GrabNotices(soup):    
    Notices = []
    for d in soup.findAll("div",class_="panelLabelViewModeTabModule"):
        Notices.append([d.a.contents,d.span.contents])

    return Notices

def ReturnButtonLinks(link,soup):

    InputTag = soup.findAll(attrs ={"value" : "Suchen"})
    URLS = []

    
    browser = mechanicalsoup.StatefulBrowser()
    for Tag in InputTag: 
        browser.open(link)
        form = browser.select_form()    
        NameTag = Tag['name']
        form.choose_submit(NameTag)
        page2 = browser.submit_selected()
        URLS.append(page2.url)
        
    return URLS


def Diver(url,Break,MaxScore):
    
    try:
        t = requests.get(url).text
    except:
        return [],0,[]
    
    soup = BeautifulSoup(t,"lxml")
    
    Notices = GrabNotices(soup)
    
    CurrentScore = len(Notices)
    
    if(Break and CurrentScore < MaxScore//2):
        return [],0,[]
    
    URLS = ReturnButtonLinks(url,soup)
    
    for Pot in soup.findAll('a'):
        
        try:
            Link = Pot["href"]
        except:
            pass
        else:
            if(Link != None):
                if(not "http" in Link 
                   and Link[:2] != "//"):
                    if(Link[0] != "/" and Link[0] != "." and url[-1] != "/"):
                        MLink = MergeLink(Revert(url,1),Link)
                    else:
                        MLink = MergeLink(url,Link)
                        
                        
                    if(not MLink in URLS):
                        URLS.append(MLink)
    
    return URLS,CurrentScore,Notices


def MergeLink(Root,Link):
    if(Link[0] == "/" or not Link[0] == "."):
        if(Root[-1] == "/" and Link[0] == "/"):
            return Root + Link[1:]
        else:
            return Root + Link
        
    if(Link[:3] == "../"):
        Depth = Link.count("../")
        return Revert(Root,Depth+1) + Link[Depth*3:]
    
def Revert(Root,Depth):
    Root = Root[::-1]
    idx = 0
    c   = 0
    while(True):
        idx = Root.find("/",idx+1)
        c += 1
        if(c >= Depth):
            return Root[idx:][::-1]

def RemoveUrlCycles(url):
    
    SUrl = url.split("/")
    
    HasCycle = False
    for i,e in enumerate(SUrl):
        if(e != '' and SUrl[i+1:].count(e) > 0):
            HasCycle = True
            break
    
    if(not HasCycle):
        return url
    
    New = [] 
    for i,a in enumerate(SUrl):
        for j,b in enumerate(SUrl[i+1:]):
            if(a == b):
                New = SUrl[:i]+SUrl[i+1+j:]
                
    NewUrl = ""
    for e in New:
        NewUrl += e
        NewUrl += "/"
    
    return NewUrl


def Crawl(url):
    FL,SC,AllNotices = Diver(url,False,0)
    MaxScore = SC
    Searched = []
    
    Depth = 1
    while(len(FL)>0):
    
        NewFL = []
        for i,link in enumerate(FL):
            
            NewLinks,Score,Notices = Diver(link,True,MaxScore)
            
            NewLinks = [RemoveUrlCycles(NLU) for NLU in NewLinks]
            
            if(MaxScore<Score):
                MaxScore = Score
            
            UpdatedNotices = False
            for Notice in Notices:
                if Notice not in AllNotices:
                    AllNotices.append(Notice)
                    
                    yield Notice
                    
                    UpdatedNotices = True
            
            for NLink in NewLinks:
                if NLink not in Searched:
                    Searched.append(NLink)
                    if(UpdatedNotices and Score >= MaxScore//2):
                        NewFL.append(NLink)
            

        FL = list(set(NewFL))
        Depth += 1





url = "https://traueranzeigen.noz.de/"

Crawler =  Crawl(url)

for Notice in Crawler:
    print(Notice)


