import numpy as np
import sys
import pandas as pd
import os
import matplotlib.pyplot as plt

dir_path = os.path.dirname(os.path.realpath(__file__))
filename = dir_path+'/mortality/Mortality_AGBLSterbewoche.csv'
print(filename)
data = pd.read_csv(filename, delimiter = ";",header=0)

BerlinData = data[data['Bundesland'] == 'Berlin']
BerlinDataJung = BerlinData[BerlinData['Altersgruppe'] == '0-64']

plt.figure()
YearData = BerlinDataJung[BerlinDataJung['Sterbejahr']==2015]
PlotData = np.array(YearData['Todesfälle'])
plt.plot(np.linspace(1,53, num=53) , PlotData)
plt.show()
