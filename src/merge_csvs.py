# Merge csvs
import glob
import os
import pandas as pd
import numpy as np
import codecs

DirPath = os.path.dirname(os.path.realpath(__file__))
def MergeCsvs(path):
    CsvPaths = glob.glob(path)

    fout = open(DirPath+"/WK/All/WK_death_data_temp.csv","a")
    for num in range(len(CsvPaths)):
        print(num)
        for line in open(CsvPaths[num],encoding = 'ISO-8859-1') :
            fout.write(line)

    fout.close()

names = None

def ReadNames(filename):
    global names
    names = []
    with codecs.open(filename, encoding='ISO-8859-1') as f:
        for line in f:
            names.append(line.split(';'))
    names = np.asarray(names)
    print(names.shape)

def GetSex(name):
    sex = names[np.where(names[:,0] == name)]
    if sex.shape == (0,2): # name is not in the list
        return -2
    if 'w' in sex[0,1]: # female
        return 0
    if 'm' in sex[0,1]: # male
        return 1
    return -1 # not specified

ReadNames('vornamen.csv')
MergeCsvs(DirPath+'/WK/*.csv')
df = pd.read_csv(DirPath+"/WK/All/WK_death_data_temp.csv",encoding = 'ISO-8859-1')
df.columns = ['Name', 'BD', 'DD','Ort']


df['Name'] = df['Name'].str.replace('Traueranzeigen', '').str.replace('Traueranzeige','')
df['BD'] = df['BD'].str.replace('\D?', '')
df['DD'] = df['DD'].str.replace('\D?', '')
df['DD'].replace('', np.nan, inplace=True)
df = df.dropna()
df['Gender'] = df['Name'].apply(lambda x: GetSex(x.split()[0]))
print(df[df['Gender'] == -2].shape)
del df['Name']
print(df)
df.to_csv(DirPath+"/WK/All/WK_death_data.csv", sep=',')
