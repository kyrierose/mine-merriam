import requests as r
from bs4 import BeautifulSoup
import random
import re
import json
import xlsxwriter

def getProxy():
    website = r.get('https://www.us-proxy.org/')
    html = website.text
    soup = BeautifulSoup(html,'html.parser')
    new_soup = soup.tbody
    var = []
    index = 0
    for i in new_soup.find_all('td'):
        var.append(i.text)
    l = []
    whileIndex = 0
    while(True):
        if (whileIndex < len(var)) and (var[whileIndex+4] == 'elite proxy' or 'anonymous' or 'transparent') :
            l.append(str(var[whileIndex])+":"+str(var[whileIndex+1]))
        else:
            break
        whileIndex += 8
    rand = random.choice(l).split(':')
    return "http://" + str(rand[0]) + ":" + str(rand[1])


def mineMerriam(url):
    m = r.get(url,proxies={'http':getProxy()})
    m_text = m.text
    soup = BeautifulSoup(m_text,'html.parser')

#finding no_of_pages per column
    page_limits = soup.find(attrs = {'class':'counters'})
#lambda expression to seperate strings
    l = [int(s) for s in page_limits.string.split() if s.isdigit()]
    no_of_pages = l[-1]
#temporary variable to hold words for single iteration for
    words = {}
#scrape words from website
    for page in range(1,no_of_pages+1):
        print('\nCurrent in Page '+str(page) +' of '+str(no_of_pages))
        req = r.get(url+'/'+str(page))
        text = req.text
        bs = BeautifulSoup(text,'html.parser')
        items = bs.find('div',class_= 'entries')
        list = items.text.split('\n')[3:-3]
        list = [x for x in list if x]
        dict_of_synonyms = getSynonyms(list)
        words.update(dict_of_synonyms)
    return words

def cycleAlpha():
    alphabets = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    for char in alphabets:
        print("\nStarted for "+char)
        words = mineMerriam("https://www.merriam-webster.com/browse/thesaurus/"+str(char))
        generate_excel_and_json_file(words, 'Synonyms'+'-'+char)
        print("Completed for "+ char)

def getSynonyms(wordList):
    dict = {}
    for word in wordList:
        url = 'https://www.merriam-webster.com/thesaurus/'+str(word)
        print("\nGetting synonym for "+str(word))
#scrape synonyms in dictionary and then return dictionary
        req = r.get(url)
        text = req.text
        bs = BeautifulSoup(text, 'html.parser')
        items = bs.find('meta',property ="og:description")
        items = items['content']
        dict[str(word)] = prettify(items)
        print(dict[word])
    return dict

def prettify(str1):
    x = str(str1.split(':')[1])
    y = x.split(',')
    z = []
    for i in y:
        z.append(i.strip())

    z[-1] = z[-1].split(' ')[0]
#removes any special character
    z[-1] = re.sub('[^A-Za-z0-9]+', '', z[-1])
    return z


def generate_excel_and_json_file(final_list,filename):
    #Creates Json File
    with open(filename +'.json', 'w') as fp:
        json.dump(final_list, fp)
    #creates Excel File
    workbook = xlsxwriter.Workbook(filename+'.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0

    for key in final_list.keys():
        row += 1
        col = 0
        worksheet.write(row, col, key)
        for item in final_list[key]:
            worksheet.write(row , col+1 , item)
            col += 1

    workbook.close()


cycleAlpha()