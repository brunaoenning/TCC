#!/usr/bin/env python
# coding: utf-8

#import library used to consult an URL
import urllib.request

#import functions BeautifulSoup to analyse the returned data from the website 
from bs4 import BeautifulSoup

#specify the URL
wiki = "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior"

#consult the website and return the html to 'page' variable
page = urllib.request.urlopen(wiki)

#parse html to 'page' variable and store it using BeautifulSoup format
soup = BeautifulSoup(page, 'html5lib')

#import the necessary libraries 
import pandas as pd
import os
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import requests, zipfile, io
import re

soup.prettify() #get all page content

list_item = soup.find_all('a', attrs={'class': 'external-link'}) #find only the 'external-link' classes

links = []
for link in list_item:
    links.append(link.get("href")) #select only the links into a vector
links

#open ELLAS file and group by year 
ellas = pd.read_csv("C:/Users/bruna/OneDrive/Documentos/Ellas/Secondary Data/secondarydata_uploaded.csv", index_col=None, encoding='latin-1', low_memory=False)
ellas['year']

#inicialize the variables
i = 0
savelinks = []

for link in links:
    exist = 0
    findall = re.findall("\d+", link) #find a number into the link to check if that year was already uploaded
    #print(findall)
    
    #instead of checking if the link exists in the folder, in order to avoid unecessary csv's stored file,
    #check if the year exists in ELLAS csv
    for year in ellas['year']:
        if int(findall[0]) == year:
            exist = 1
    
    #if it didn't exist AND if the year is bigger then 2008
    if exist == 0 and int(findall[0])>2008:
        savelinks.append(links[i])
        
    i = i + 1
savelinks

#create folder with all the links zip files
folder = "C:/Users/bruna/OneDrive/Documentos/Ellas/Secondary Data/INEP"
os.makedirs(folder, exist_ok=True)
for link in savelinks:
    disable_warnings(InsecureRequestWarning) #Fix SSLError https://stackoverflow.com/questions/72188582/sslerror-max-retries-exceeded-with-url-error-how-to-fix-this
    folder = "C:/Users/bruna/OneDrive/Documentos/Ellas/Secondary Data/INEP"
    r = requests.get(link, verify=False)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    os.makedirs(folder, exist_ok=True)
    z.extractall(folder)

isEqual = 0
num = 0

#comparing excel files https://acervolima.com/python-comparacao-de-arquivos-do-excel/
#it's necessary to compare the first row data after row 9  
for directory, subfolders, files in os.walk(folder):
    for file in files:
        if(file.startswith("dicionário") or file.startswith("dicionario")):
            print("Checking "+directory + "/" + file+"...")
            string1 = directory + "/" + file
            num = num + 1
            string2 = "C:/Users/bruna/OneDrive/Documentos/Ellas/Secondary Data/dicionário_dados_comparativo.xlsx"
            sheet1 = pd.read_excel(string1)
            sheet2 = pd.read_excel(string2) 
            if (os.path.exists(string1)):
                print("Sheet file exist")
            else:
                print("Sheet file DO NOT exist")
                break
    #         if (os.path.exists(string2)):
    #             print("Second file exists")
            for i,j in zip(sheet1,sheet2): 
                if i=='Unnamed: 0': #Only data from the first column
                    a,b =[],[] 
                    for m, n in zip(sheet1[i],sheet2[j]): 
                        a.append(m) 
                        b.append(n) 
            #             a.sort() 
            #             b.sort() 
                    for m, n in zip(range(len(a)), range(len(b))): 
                        if m > 8:
                            if a[m] != b[n]: 
                                print('Column name : \'{}\' and Row Number : {}'.format(i,m))
                                isEqual = 1
if(isEqual == 0):
    print("Success :)") #if all the files are using the acording format


