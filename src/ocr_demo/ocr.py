Death = "Unsere Tante Irma nach Krankheit früh ist krank plötzlich ist am 11. Juni 2015 gestorben. Sie wurde geboren am 25.1.1900. Beerdigung 26. Juli 2015"
# Krankheit, lang, schwer, kurze, viel zu früh, plötzlich, unerwartet, schweres Leiden
import re
import datetime
import numpy as np
import mechanicalsoup
from bs4 import BeautifulSoup
import requests
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

ClassesDeath = ['"Lange Krankheit","Kurze Krankheit", "plötzlich", "neutral" ']
def month_string_to_number(string):
    m = {
        'Januar': 1,'Februar': 2,'März': 3,'April':4,'Mai':5,'Juni':6,'Juli':7,'August':8,'September':9,'Oktober':10,'November':11,
         'Dezember':12
        }
    try:
        out = m[string]
        return out
    except ValueError:
        pass

def YieldDates(DateStr):

    Regex = ".?[0-9]\..*?.?[1-3][0-9][0-9][0-9]"
    Dates = []
    for match in re.findall( Regex,DateStr):
        Separated =re.findall(r'\S+',match)
        #Line = re.sub('\.','',Separated[0])
        if len(Separated) >1:
            Line = re.sub('\.','',Separated[0])
            Day = int(Line)
            Month = month_string_to_number(Separated[1])
            Year = int(Separated[2])


            Dates.append(datetime.date(Year,Month,Day))
        elif len(Separated) == 1:
            Line =re.split(r'\.', match)
            Year = int(Line[2])
            Month = int(Line[1])
            Day = int(Line[0])
            Dates.append(datetime.date(Year,Month,Day))
    # minimum date found is BirthDate
    BirthDate = np.min(Dates)
    Dates.remove(BirthDate)
    DeathDate = np.min(Dates)

    return BirthDate, DeathDate

def YieldTags(Announcement):
    Illness = ['krank','Krank','hölle','Hölle', 'Leide','leide', 'Pflege','pflege']
    Unexpected = ['plötzlich','Plötzlich','kurz','Kurz', 'früh','Früh']
    Long = ['lang','Lang']
    Numbers = []
    ill = 0
    for i in range(len(Illness)):
        ill = ill + Announcement.count(Illness[i])
    sudden = 0
    for i in range(len(Unexpected)):
        sudden = sudden + Announcement.count(Unexpected[i])
    longer = 0
    for i in range(len(Long)):
        longer = longer + Announcement.count(Long[i])

    if ill != 0 and (ill + sudden) > ill:
        Tag = 'Kurze Krankheit'
    elif ill != 0 and (ill + longer) > ill:
        Tag = 'Lange Krankheit'
    elif sudden != 0:
        Tag = 'Plötzlich'
    else:
        Tag = 'Neutral'

    return Tag

def CallOCR(link):
    browser = mechanicalsoup.StatefulBrowser()
    page = browser.open('http://www.free-ocr.com/')
    form = page.soup.form

    form.find("input",{"name": "userfile_url"})["value"] = link
    form.find("input",{"name": "language[]"})["value"] = 'deu'
    response = browser.submit(form, page.url)

    soup = BeautifulSoup(response.text, 'html.parser')

    print(response.text)


def main():
    #Links = ["http://www.bestattungsdienst-uhl.de/mediathek/muster-todesanzeigen/muster-1-4spaltig.jpg"]
    #for i in len(Links):
    #test = '/home/cath/Pictures/Muster.png'
    #tessdata_dir_config = '--tessdata-dir "/usr/share/tesseract-ocr/tessdata"'
    #string = pytesseract.image_to_string(Image.open(test), lang = 'eng')
    #print(string)
    with open('Muster.txt', 'r') as myfile:
        string=myfile.read().replace('\n', ' ')
    print(string)
    BirthDate, DeathDate = YieldDates(string)
    Tag = YieldTags(string)

    print(BirthDate, DeathDate, Tag)
    #print(ReturnButtonLink('https://www.ovbtrauer.de/'))
    #print(yield_dates(Death))
    #print(YieldTags(Death))

if __name__ == "__main__":
    main()
