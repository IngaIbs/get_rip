import numpy as np
import sys
import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime

DirPath = os.path.dirname(os.path.realpath(__file__))
MortalityFilename = DirPath+'/mortality/Mortality_AGBLSterbewoche.csv'
MortalityData = pd.read_csv(MortalityFilename, delimiter = ";",header=0)

CrawlerFilename = DirPath+'/mortality/DataMerged.csv'
CrawlerData = pd.read_csv(CrawlerFilename, delimiter = ",", names= ["Deathdate","Name","Age"])

#BerlinDataJung = BerlinData[BerlinData['Altersgruppe'] == '0-64']
#YearData = BerlinDataJung[BerlinDataJung['Sterbejahr']==2015]

# Only 2015 mortality
BerlinData = MortalityData[MortalityData['Bundesland'] == 'Berlin']
YearFifteen = BerlinData[BerlinData['Sterbejahr']==2015]
BerlinDataAllYear = pd.DataFrame(index = np.arange(1,54),columns= ['Jahr','Sterbewoche','Tote'])
for i in np.arange(1,54):
    BerlinDataAllYear.ix[i,'Sterbewoche'] = i
    BerlinDataAllYear.ix[i,'Tote'] = Year.loc[Year['Sterbewoche'] == i]['Todesfälle'].sum()
    BerlinDataAllYear.ix[i,'Jahr'] = 2015

# Only 2015 crawler data

CrawlerArray = np.array(CrawlerData['Deathdate'])
CrawlerYear = CrawlerArray[(CrawlerArray<20160000) & (CrawlerArray>20150000)]
CrawlerDates = np.zeros(CrawlerYear.shape[0])
for i in np.arange(CrawlerYear.shape[0]):
    DateInt = CrawlerYear[i]
    CrawlerDates[i]=datetime.date(int(str(DateInt)[0:4]),int(str(DateInt)[-4:-2]),int(str(DateInt)[-2:])).isocalendar()[1]

CrawlList = list(CrawlerDates)
CrawlPlotData = np.zeros(53)
for i in np.arange(53):
    CrawlPlotData[i] = CrawlList.count(i+1)
print(np.max(CrawlPlotData), np.min(CrawlPlotData))

# plot
plt.figure()
AllYear = np.array(BerlinDataAllYear['Tote'])
PlotData = AllYear/np.max(AllYear)
plt.plot(np.linspace(1,53, num=53) , PlotData)
plt.plot(np.linspace(1,53, num=53) , CrawlPlotData/np.max(CrawlPlotData))
plt.show()
