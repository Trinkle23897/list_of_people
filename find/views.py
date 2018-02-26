from django.shortcuts import render
from bs4 import BeautifulSoup as bs
import os
import re
import random
import pickle as pkl

# Create your views here.
search_html='''<form method="get" action="/find/" align="center">
        <table style="width:34em" align="center">
        <tr><th style="text-align:left; color:%s">Search: </th><td>
            <input type="text" name="fsrch" placeholder="Search text"          title="Search text"       id="Input1" tabindex="1" size="80">
        </td></tr>
        <tr><th style="text-align:left; color:%s">Name:</th><td>
            <input type="text" name="fname" placeholder="Example: Alan Turing" title="Search name"       id="Input2" tabindex="2" size="80">
        </td></tr>
        <tr><th style="text-align:left; color:%s">Nation:</th><td>
            <input type="text" name="fnatn" placeholder="Example: American"    title="Search nation"     id="Input3" tabindex="3" size="80">
        </td></tr>
        <tr><th style="text-align:left; color:%s">Occupation:</th><td>
            <input type="text" name="foccu" placeholder="Example: actor"       title="Search occupation" id="Input4" tabindex="4" size="80">
        </td></tr>
        <tr><th style="text-align:left; color:%s">Birthday:</th><td>
            <input type="text" name="fborn" placeholder="Example: 1926-08-17"  title="Search birthday"   id="Input5" tabindex="5" size="80">
        </td></tr>
        <tr><th style="text-align:left; color:%s">Deathdate:</th><td>
            <input type="text" name="fdday" placeholder="Example: 1989-06-04"  title="Search deathdate"  id="Input6" tabindex="6" size="80">
        </td></tr>
            %s
        <tr><td colspan="2" align="center"><br>
            <input type="submit" name="go" value="Search" title="Search" id="searchButton" style="display: inline-block;margin-top: 15px;margin-bottom: 10px;vertical-align: middle;color: rgb(255, 255, 255);background-color: #00BFFF;text-align: center;cursor: pointer;white-space: nowrap;box-shadow: rgba(0, 0, 0, 0.12) 0px 2px 6px, rgba(0, 0, 0, 0.24) 0px 1px 2px;border-width: initial;border-style: none;border-color: initial;border-image: initial;outline: 0px;padding: 8px 18px;overflow: hidden;text-decoration: none;transition: 0.2s ease-out;border-radius: 2px;">
        </td></tr>
        </table>
    </form>'''

with open("data/cache.pkl","rb") as fi:
    people=pkl.load(fi)
tot_num=len(people)
print(tot_num)
# [name,category,birthday,deathdate,nationality,occupation]

rank=[]
for i in people:
    rank.append([0]+i)
highlight=[]

def getinitpage(request):
    soup=bs('''<html><head>
        <style type="text/css">
        body {background-image:url(https://git.thusaac.org/trinkle/wallpaper/raw/master/mbuntu-2.jpg);background-size:1600px 900px;}
        </style>
        <title>Search people - Powered by n+e</title></head><body><br><br><br><br><br><br><br><h1 align="center">Search for list of people in Wikipedia</h1><br><br>'''
        #%(os.getcwd()+'/data/1.jpg')
        +search_html%('white','white','white','white','white','white',r'{% csrf_token %}')+'</body></html>','html.parser')
    with open("data/person.html","w") as fout:
        fout.write(soup.prettify())
    return render(request,"person.html")


def getpage(request,str2): #del str1
    print('---------')
    global highlight
    print(highlight)
    print(str2)
    #
    #str1=people[i][1]
    #str2=people[i][0]
    # calc category
    category=[]
    str1=""
    for person in people:
        if person[0]==str2:
            print("classfication: ",person[1])
            category.append(person[1])
            str1=person[1]
    print(str1)
    try:
        with open("data/"+str1+'/'+str2) as f:
            html=f.read()
        soup=bs(html,'html.parser',from_encoding='utf-8')
    except:
        return getinitpage(request)

    # set style
    soup.table['align']="center"
    soup.table['style']="width:50em"

    # fix links
    for link in soup.find_all(href=re.compile("^/wiki/")):
        link["href"]="https://en.wikipedia.org"+link["href"]
    for link in soup.find_all(href=re.compile("^#")):
        if link.string.find('[')!=-1:
            link.decompose()
        else:
            link["href"]="https://en.wikipedia.org/wiki/"+str2+link["href"]

    # add category to table
    tag1=soup.new_tag("th",scope='row');tag1.insert(1,'Category')
    tag2=soup.new_tag('td');#tag2.insert(1,category)
    tag2.insert(0,('000000'.join(category)).replace('_',' '))
    #    for li in category:
    #        tag2.insert(0,li.replace('_',' '))
    #    tag2.string=tag2.string.replace(' List','\nList')
    tag=soup.new_tag("tr")
    tag.append(tag1)
    tag.append(tag2)
    try:
        soup.findAll('th',scope='row')[-1].parent.append(tag)
    except:
        print("qwq")

    # add ID to table
    ID=-1
    tag1=soup.new_tag("th",scope='row');tag1.insert(1,'ID')
    tag2=soup.new_tag('td');#tag2.insert(1,category)
    for i in range(tot_num):
        if people[i][0]==str2:
            tag2.insert(1,"hhhhhh")
            ID=i
            break
    tag=soup.new_tag("tr")
    tag.append(tag1)
    tag.append(tag2)
    try:
        soup.findAll('th',scope='row')[-1].parent.append(tag)
    except:
        print("qwq2")
    # set table stylesheet
    tmp=1
    for cont in soup.findAll('th',scope="row"):
        #print(cont)
        tmp+=1
        if tmp%2==0:
            #cont['style']="text-align:left"
            cont['style']="text-align:left; background-color:#E7E4E4"
            try:
                if cont.next_sibling!='\n':
                    cont.next_sibling['style']="background-color:#E7E4E4"
                else:
                    cont.next_sibling.next_sibling['style']="background-color:#E7E4E4"
            except:
                print("Emmm")
        else:
            #cont['style']="text-align:left; background-color:#E7E4E4"
            cont['style']="text-align:left"
    
    # set highlight word
    #highlight=['1','s','Khan']
    for st in highlight:
        p=re.compile(r'\b'+st+r'\b',re.I)
        for tag in soup.findAll(re.compile(""),text=p):
            tag.string=p.sub(r'333333'+st+r'444444',tag.string)
    highlight=[]
    # set title
    # head=soup.new_tag("head")
    # title=soup.new_tag("title")
    # title.insert(0,str2.replace('_',' '))
    # head.append(title)
    # soup.append(head)

    # set title stylesheet
    fn=soup.find(class_="fn")
    if fn.name=="span":
        fn=fn.parent
    fn['style']="text-align:center;font-size:125%;font-weight:bold;font-size:larger; background-color: #ddd; color: #666; padding: 4px; border-bottom: 2px solid #ccc;"
    search=bs('<br><hr><br>'+search_html%('black','black','black','black','black','black',r'{% csrf_token %}'),'html.parser')
    #    text=soup.get_text().split()
    #    text=re.sub(' +',' ',text)
    #    text=re.sub('\n+','\n',text)
    #    text=re.sub('[\n ]+','\n',text)
    pre=ID
    while people[pre][0]==people[ID][0]:
        pre-=1
    nxt=ID
    while people[nxt][0]==people[ID][0]:
        nxt+=1
    with open("data/person.html","w") as fout:
        fout.write('''<head><title>%s</title><style type="text/css">body { background-color: #f2f2f7; }</style></head><body>'''%str2.replace('_',' ')
            +soup.prettify()
                .replace('333333','<span style="background-color:yellow">')
                .replace('444444','</span>')
                .replace('000000','<br>')
                .replace('hhhhhh','<a href=/find/%d>%d</a>'%(ID,ID))
                +'''<div align="center"><input type=button onClick="location.href='/find/%d'" value='Previous' style="display: inline-block;margin-top: 15px;margin-bottom: 10px;vertical-align: middle;color: rgb(255, 255, 255);background-color: #00BFFF;text-align: center;cursor: pointer;white-space: nowrap;box-shadow: rgba(0, 0, 0, 0.12) 0px 2px 6px, rgba(0, 0, 0, 0.24) 0px 1px 2px;border-width: initial;border-style: none;border-color: initial;border-image: initial;outline: 0px;padding: 8px 18px;overflow: hidden;text-decoration: none;transition: 0.2s ease-out;border-radius: 2px;">
                <input type=button onClick="location.href='/find/%d'" value='Next' style="display: inline-block;margin-top: 15px;margin-bottom: 10px;vertical-align: middle;color: rgb(255, 255, 255);background-color: #00BFFF;text-align: center;cursor: pointer;white-space: nowrap;box-shadow: rgba(0, 0, 0, 0.12) 0px 2px 6px, rgba(0, 0, 0, 0.24) 0px 1px 2px;border-width: initial;border-style: none;border-color: initial;border-image: initial;outline: 0px;padding: 8px 18px;overflow: hidden;text-decoration: none;transition: 0.2s ease-out;border-radius: 2px;"></div>
                '''%(pre,nxt)
                +search.prettify()+'</body>')
    #    print(soup.prettify())
    return render(request,"person.html")

def query(request):
    #print('POST:  ',request.POST)
    print('get:   ',request.GET)
    try:
        search     = request.GET['fsrch']
        born       = request.GET['fborn']
        occupation = request.GET['foccu']
        nation     = request.GET['fnatn']
        name       = request.GET['fname']
        deathdate  = request.GET['fdday']
    except:
        return getinitpage(request)
    global highlight
    global rank
    # [name,category,birthday,deathdate,nationality,occupation]
    rank=[]
    for i in range(tot_num):
        rank.append([0,i]+people[i])
    for i in range(tot_num):
        rank[i][0]=0.
        if people[i][2]:
            rank[i][0]=2+random.random()

    # search
    if search:
        highlight+=search.split()
        born+=search
        deathdate+=search
        occupation+=search
        nation+=search
        name+=search
    # born
    if born:
        highlight+=[born]
        for i in range(tot_num):
            if people[i][2]==born:
                rank[i][0]+=5.
    # occupation
    occ_num=len(occupation.split())
    if occ_num:
        highlight+=occupation.split()
        for i in range(tot_num):
            for occ in occupation.split():
                if occ.lower() in people[i][5].lower().split():
                    rank[i][0]+=5./occ_num
                elif occ.lower() in people[i][1].lower().split('_'):
                    rank[i][0]+=5./occ_num
    # nation
    nation_num=len(nation.split())
    if nation_num:
        highlight+=nation.split()
        for i in range(tot_num):
            for nat in nation.split():
                if nat.lower() in people[i][4].lower().split():
                    rank[i][0]+=5./nation_num
    # name
    name_num=len(name.split())
    if name_num:
        highlight+=name.split()
        for i in range(tot_num):
            for nm in name.split():
                if nm.lower() in people[i][0].lower().split('_'):
                    rank[i][0]+=5./name_num
    # deathdate
    if deathdate:
        highlight+=[deathdate]
        for i in range(tot_num):
            if people[i][3]==deathdate:
                rank[i][0]+=5
    print("highlight:  ",highlight)
    rank.sort()
    rank.reverse()
    str=""
    lst=set()
    for i in range(tot_num):
        if(rank[i][0]>3):
            print(rank[i][0])
        if rank[i][0]>3 and rank[i][2] not in lst:
            lst.add(rank[i][2])
        elif rank[i][2] in lst:
            rank[i][0]=0
    rank.sort()
    rank.reverse()
    cnt=0
    for i in range(tot_num):
    	if rank[i][0]>=1:
    		cnt+=1
    print("cnt:  ",cnt)
    cnt=0
    small=rank[0][0]/2.
    for i in range(tot_num):
        if cnt<50 and rank[i][0]>3 and rank[i][0]>small:
            # [x,x,name,category,birthday,deathdate,nationality,occupation]
            str+='<tr><th><a href="/find/%d">%s</a></th><td>'%(rank[i][1],rank[i][2].replace('_',' '))
            if rank[i][3]:
                str+='Category: %s<br>'%rank[i][3].replace('_',' ')
            if rank[i][4]:
                str+=rank[i][4]
            else:
                str+='?'
            str+=' ~ '
            if rank[i][5]:
                str+=rank[i][5]
            str+='<br>'
            if rank[i][6]:
                str+='Nationality: %s<br>'%rank[i][6]
            if rank[i][7]:
                str+='Occupation: %s<br>'%rank[i][7]
            str+='</td></tr>'
            cnt+=1
            # if cnt%5==0:
            #     str+='<hr>'
            # else:
            #     str+='<br>'
            #print(rank[i][2],rank[i][0])
    str='<table style="width:40em" align="center" bgcolor="#DBDBDB">'+str+'</table>'
    soup=bs('''<html><head>
        <style type="text/css">
        body { background-image: url('http://www.mekau.com/wp-content/uploads/2016/07/5-120601095139-50.gif'); background-repeat: repeat; background-position: top left; background-attachment: scroll; }
        </style>
        <title>Search people - Powered by n+e</title></head><body><h1 align="center">Search result</h1><br><hr><br>'''
        +str+'<br><hr><br>'
        +search_html%('black','black','black','black','black','black',r'{% csrf_token %}')+'</body></html>','html.parser')
    with open("data/person.html","w") as fout:
        fout.write(soup.prettify())
    return render(request,"person.html")

def find(request):
    return getnumber(request,650)

def getnumber(request,num):
    y=int(num)%tot_num
    return getpage(request,people[y][0])
    # for i in range(tot_num):
    #     if person[i][0]==name[y]:
    #         print(person[i][0])

