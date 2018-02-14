import codecs
import numpy as np

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
print(GetSex('Anna'))
print(GetSex('Kim'))
print(GetSex('Eike'))
print(GetSex('Maria'))
print(GetSex('Peter'))
print(GetSex('Sören'))
print(len(np.where(names[:,1] == 'unspezifisch\r\n')[0]))
print(len(np.where(names[:,1] == 'männlich\r\n')[0]))
print(len(np.where(names[:,1] == 'weiblich\r\n')[0]))

print((names[np.where(names[:,1] == 'unspezifisch\r\n')][:50,0]))
        
    
