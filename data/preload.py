import os
import re
import sys
import pickle as pkl
from bs4 import BeautifulSoup as bs

all=[f for f in os.listdir() if f[:8]=="List_of_"]
people=[]
cnt=0

for dir in all:
    name=os.listdir(dir)
    #if cnt>0:
    #    break
    for table in name:
        cnt+=1
        if cnt%100==0:
            print(cnt)
        with open(dir+'/'+table) as f:
            soup=bs(f.read(),"html.parser")
        for link in soup.find_all(href=re.compile("^#")):
            link.decompose()
        bday=soup.find(class_="bday")
        if bday:
            bd=bday.getText().replace('\n',' ')
            bd=' '.join(bd.split())
            bd.replace(' ,',',')
        else:
            bd=""
        dday=soup.find(class_="dday deathdate")
        if dday:
            dd=dday.getText().replace('\n',' ')
            dd=' '.join(dd.split())
            dd.replace(' ,',',')
        else:
            dd=""
        nation=soup.find("th",string=re.compile("Nationality"))
        if nation:
            bn=nation.findNextSibling().getText().replace('\n',' ')
            bn=' '.join(bn.split())
            bn.replace(' ,',',')
        else:
            bn=""
        occupation=soup.find("th",string=re.compile("Occupation"))
        if occupation:
            bocc=occupation.findNextSibling().getText().replace('\n',' ')
            bocc=' '.join(bocc.split())
            bocc.replace(' ,',',')
        else:
            bocc=""
        info=[table,dir,bd,dd,bn,bocc.lower()]
        people.append(info)
#        if cnt>0:
#            break

print(233)
people.sort()
#for i in people:
#    print(i)

with open("cache.pkl","wb") as fo:
    pkl.dump(people,fo)
