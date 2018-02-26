import re
import os
import sys
import time
import random
import requests
from bs4 import BeautifulSoup

sum_=0

def getpage(url,sum_):
    print('Scan: '+url)
    rt=url.split('/')[-1]
    os.system('mkdir %s'%rt)
    if rt.find('(')!=-1 :
        return 0
    html=requests.get(url).content
    soup=BeautifulSoup(html,'html.parser',from_encoding='utf-8')
    cnt=0
    tot=0
    for link in soup.find_all(href=re.compile("/wiki/")):
        st=link.get('href')
        if st[:6]!="/wiki/" or st.find(':')!=-1:
            continue
        filename=st.split('/')[-1]
        if os.path.isfile(rt+'/'+filename)==True:
            continue
        tot+=1
        try:
            h=requests.get('https://en.wikipedia.org'+st).content
        except:
            continue
    #    if cnt>5:
    #        break;
        s=BeautifulSoup(h,'html.parser',from_encoding='utf-8')
        info=s.find(class_='infobox biography vcard')
        if info==None:
            info=s.find(class_='infobox vcard')
        if info!=None:
            cnt+=1
            sum_+=1
            print("%4d %4d %5d %s"%(cnt,tot,sum_,st))
            with open(rt+'/'+filename,"w") as f:
                f.write(info.prettify())
    #        print(info)
    return sum_

html=requests.get('https://en.wikipedia.org/wiki/Lists_of_actors').content
soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

urls=soup.find_all(href=re.compile("/wiki/List_of_"))
#urls.reverse()

flag=0
for link in urls[:]:
    if link.get('href')=='/wiki/List_of_film_and_television_directors':
        flag=1
    if flag==1:
        sum_=getpage('https://en.wikipedia.org'+link.get('href'),sum_)

