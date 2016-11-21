
# coding: utf-8

# In[1]:

import urllib2
from bs4 import BeautifulSoup


# In[2]:

url_etab='https://www.tripadvisor.fr/Restaurants-g187147-Paris_Ile_de_France.html'
url_etabs=['https://www.tripadvisor.fr/Restaurants-g187147-Paris_Ile_de_France.html']
for i in range(30,200,30):
    url_etabs.append(url_etab+"/Restaurants-g187147-oa"+str(i)+"-Paris_Ile_de_France.html")#7 premiers pages


# In[3]:


#"listing listingIndex-1 first"
def carac_row(ch):
    etab=etabs.find('div', {"class" : ch}).find('div', {"class" : "shortSellDetails"})
    etab_title=etab.find('a').find(text=True)#1er titre
    etab_url=str(etab.find('a', {"target" : "_blank"})).split("\"")[3]
    etab_note=etab.find('div', {"class" : "rating"}).find('img')
    etab_note=float(str(etab_note).split(" ")[1].split("\"")[1].replace(",","."))
    etab_fourch=etab.find('div', {"class" : "priceBar"}).find('span')
    etab_fourch=str(etab_fourch).split("span>")[1].split("-")
    l1=[]
    for i in etab_fourch:
        l1.append(i.count("\xe2\x82\xac"))
    etab_cuis=etab.find('div', {"class" : "cuisines"})
    l2=[]
    for e in etab_cuis.find_all("a"):
        l2.append (e.find(text=True))
    for e in etab_cuis.find_all("span"):
        l2.append (e.find(text=True))
    res=[]
    res.append(etab_title)
    res.append(etab_note)
    res.append(l1)
    res.append(l2)
    res.append(etab_url)
    return res


# In[4]:

listingIndex=["listing listingIndex-1 first"]
for i in range(2,31):
    listingIndex.append("listing listingIndex-"+str(i))


# In[5]:

nom=[]
note=[]
fourchette=[]
cuis=[]
url=[]
for u in url_etabs:
    page = urllib2.urlopen(u)#query the page and return ahtml page
    soup = BeautifulSoup(page)
    etabs=soup.find('div', {"id" : "EATERY_SEARCH_RESULTS"})
    for l in listingIndex:
        try:
            carac=carac_row(l)
            nom.append(carac[0])
            note.append(carac[1])
            fourchette.append(carac[2])
            cuis.append(carac[3])
            url.append("https://www.tripadvisor.fr/Restaurants-g187147-Paris_Ile_de_France.html"+carac[4])
        except Exception, e:
            print("Une petite erreur car certaines valeurs ne sont pas bien formatés c'est pas grave! on va les remplacer par --")


# In[6]:

import pandas as pd
df_carac=pd.DataFrame(nom,columns=['nom'])
df_carac['note']=note
df_carac['fourchette']=fourchette
df_carac['cuis']=cuis
df_carac['url']=url
df_carac


# In[7]:

df_carac.url[0]


# In[8]:

Titres = {}
Commentaires = {}
Notes = {}


# In[9]:

### TEST SELENIUM IDEA #####
#==============================================================================
# ### pip install selenium	
# #from contextlib import closing
# #from selenium.webdriver import Firefox # pip install selenium
# #from selenium.webdriver.support.ui import WebDriverWait
# #from selenium.webdriver.common.by import By
# #from selenium.webdriver.support import expected_conditions as EC
# 
# ## use firefox to get page with javascript generated content
# #with closing(Firefox()) as driver:
# #    driver.get("http://www.att.com/shop/wireless/devices/smartphones.html")
# #    button = driver.find_element_by_id('deviceShowAllLink')
# #    button.click()
# #    # wait for the page to load
# #    element = WebDriverWait(driver, 10).until(
# #    EC.invisibility_of_element_located((By.ID, "deviceShowAllLink"))
# #    )
# #    # store it to string variable
# #    page_source = driver.page_source
# #
# #soup = BeautifulSoup(page_source)
# #items = soup.findAll('div', {"class": "list-item"})
# #print "items count:",len(items)
# #
# #############MARCHE PAS##########################################################""
# #with closing(Firefox()) as driver:
# #    driver.get("https://www.tripadvisor.fr/Restaurant_Review-g187147-d10514254-Reviews-Les_Apotres_de_Pigalle-Paris_Ile_de_France.html")
# #    expectedText = "taLnk hvrIE6";
# #    els = driver.find_elements_by_xpath("//span[@class='partnerRvw']/span");
# #    for i in els :
# #        i.click()
# #
# ##    for i in els :
# ##        i.find_element_by_partial_link_text("Plus").click()
# ##    # wait for the page to load
# #    element = WebDriverWait(driver, 30)
# #    # store it to string variable
# #    page_source = driver.page_source
# #
# #soup = BeautifulSoup(page_source)
# #items = soup.findAll(True, {"class": "entry"})
# #print "items count:",len(items)
# #items
# 
#==============================================================================


# In[10]:

n_etab=50
import lxml
import requests
##lxml est + utilisé pour les moteurs de recherche. 
from lxml import html
#from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

Titres = []
allTitres={}
Commentaires = []
allCommentaires={}
#Notes = []
#allNotes={}

##les commentaires ne sont pas tous pris, j'ai compris pourquoi : les derniers commentaires de chaque restaurant sont traduits de l'anglais
## Ils n'ont pas été pris en compte dans le scraping. mais ça nous fait déjà une bonne base alors c'est bon.

#url = "https://www.tripadvisor.fr/Restaurant_Review-g187147-d10514254-Reviews-Les_Apotres_de_Pigalle-Paris_Ile_de_France.html"
#url = "https://www.tripadvisor.fr/Restaurant_Review-g196560-d782500-Reviews-Chez_Madeleine-Boulogne_Billancourt_Hauts_de_Seine_Ile_de_France.html"

#resolution du prob d'adresse
for j in range(0,len(url)):
    url[j] = url[j].replace('/Restaurants-g187147-Paris_Ile_de_France.html','')
#construire des dictionnaires pour 50 etab:
for k in range(0,n_etab):   
    url2 = url[k]#for each url
    page = requests.get(url2)
    hp = lxml.etree.HTMLParser(encoding='utf-8')
    tree = html.fromstring(page.content, parser=hp)
    
    s = url2.find('Reviews')+7
    
    Number = tree.xpath('//div[@class="pageNumbers"]/a/@data-page-number')
    #Number = Number[len(Number)-1]
    #Number = int(unicode(Number).encode('utf8'))
    #tot = Number * 10
    if(Number <3):
        Number = Number[len(Number)-1]
        Number = int(unicode(Number).encode('utf8'))
        tot = Number * 10
        
    if(Number>=3):
         tot = 30
    
    Commentaires=[]
    Titres=[]
    
    Titres = Titres + tree.xpath('//span[@class="noQuotes"]/text()')


    Commentaires = Commentaires + tree.xpath('//div[@class="entry"]/p[@class="partial_entry"]/text()')
    Commentaires = [i for i in Commentaires if i!= "\n"]
    
    #Notes = Notes + tree.xpath('//div[@class="rating reviewItemInline"]/span[@class="rate sprite-rating_s rating_s"]/img/@alt') 
    for i in range(10,tot,10):
               
        urln = url2[0:s]+'-or'+str(i)+url2[s:len(url2)]
        page = requests.get(urln)
        
        tree = html.fromstring(page.content)
        Titres = Titres + tree.xpath('//span[@class="noQuotes"]/text()')
        
        
        Commentaires = Commentaires + tree.xpath('//div[@class="entry"]/p[@class="partial_entry"]/text()') 
        Commentaires = [i for i in Commentaires if i!= "\n"]
    
        #Notes = Notes + tree.xpath('//div[@class="rating reviewItemInline"]/span[@class="rate sprite-rating_s rating_s"]/img/@alt') 
    allTitres[k]=Titres
    allCommentaires[k]=Commentaires
    #allNotes[k]=Notes   
    


# In[11]:

#allInOnCom[0]


# In[12]:

allInOnCom={}
for k in range(0,n_etab): 
    allInOnCom[k]=''.join(allCommentaires[k])
#allInOnNote={}
#for k in range(0,n_etab): 
#    allInOnNote[k]=''.join(allNotes[k])
allInOnTitre={}
for k in range(0,n_etab): 
    allInOnTitre[k]=''.join(allTitres[k])
allInOnComTitre={}
for k in range(0,n_etab): 
     allInOnComTitre[k]=(''.join(allCommentaires[k])).join(allTitres[k])


# In[13]:

import unicodedata
import string
def change(ch):
    x = unicodedata.normalize('NFKD', ch).encode('ascii','ignore')
    x = x.replace('\n',' ')
    return x


# In[ ]:




# In[14]:

for k in range(0, n_etab):
    allInOnComTitre[k] = change(allInOnComTitre[k])


# In[15]:

allInOnComTitre[7] #3 pages de commentaires assemblées pour restaurant 8 (i = 7)


# In[16]:

df_comment=pd.DataFrame(nom[0:n_etab],columns=['nom'])
df_comment['titre_comment']=""


# In[17]:

for i in range(0,n_etab):
    df_comment.titre_comment[i]=allInOnComTitre.get(i).encode('ascii', 'ignore').replace("\'"," ").replace("-"," ")


# In[18]:

type(df_comment.titre_comment[49]) #string propre


# In[19]:

for j in range(0,50):
    df_comment.titre_comment[j].translate(None, string.punctuation)


# In[20]:

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
from collections import Counter
#application du TF:
#eliminer la ponctuation: 
def get_result(ch):
    low=ch.lower()#to lower
    nopunc=low.translate(None, string.punctuation)#eliminer la ponctuation
    
    tokens=nltk.word_tokenize(nopunc)#from string to list
    
    filtered = [w for w in tokens if not w in stopwords.words('French')]#enlever les mots pronominaux, de liaison ....
    filtered = [x for x in filtered if not x in stopwords.words('English')] #enlever les mots anglais (sans ponctuation, le a par exemple)
    
    stemmer = PorterStemmer()
    stemed=[]
    for item in filtered:
        stemed.append(stemmer.stem(item))#retourner les mots à leurs racine/radical
    #return ' '.join(stemed)#retourne 
    count = Counter(stemed)
    return count.most_common(100)


# In[ ]:




# In[21]:

#from nltk.probability import FreqDist
#import re
#from nltk.tokenize.regexp import RegexpTokenizer

## Comptage des mots à la création
#fdist = FreqDist(nltk.word_tokenize(df_comment.titre_comment[0].lower().translate(None, string.punctuation)))
#y = fdist.items()[:200]
#sorted(y, key=lambda a: a[1], reverse=True) #fréquence des mots décroissante


# In[22]:

z = get_result(df_comment.titre_comment[5])


# In[23]:

#Visualisation sous wordle, copier-coller ce qu'il y a ci-dessous dans l'interface avancée.
for l in z :
         print "%s:%d" % (l[0], int(l[1]*10000))
    


# In[24]:

#généralisation du processus
def nuage_mots(nb):
    z = get_result(df_comment.titre_comment[nb])
    #Visualisation sous wordle 
    for l in z :
         print "%s:%d" % (l[0], int(l[1]*10000))
    
    


# In[ ]:




# In[25]:

#x =df_comment.titre_comment[0]


# In[26]:

#x.encode('utf-8')


# In[27]:

#from nltk.corpus import stopwords
#import string
#text=''
#text = ' '.join([word for word in allInOnCom[0].split() if word not in stopwords.words("french")])
#exclude = set(string.punctuation)
#text = ''.join(ch for ch in text if ch not in exclude)


# In[28]:

#import re
#pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
#text = pattern.sub('', text)

