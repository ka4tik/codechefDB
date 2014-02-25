from bs4 import BeautifulSoup
import urllib
import urllib2
import json
import sqlite3
import sys
import os
db=sqlite3.connect('codechef.db')
c=db.cursor()
c.execute('''DROP TABLE users''')
c.execute('''CREATE TABLE users
             (username text primary key,
             name text,
             url text,
             long_rating real,
             short_rating real,
             long_global_rank integer,
             long_country_rank integer,
             short_global_rank integer,
             short_country_rank integer,
             country text,
             state text,
             city text,
             motto text,
             link text,
             about_me text,
             student_professional text,
             institution text
             )''')

fileNames = os.listdir('./users')
#fileNames=fileNames[:2]
def readFile(fileName):
    contents = []
    f = open(fileName)
    for line in f:
        contents.append(line)
    f.close()
    result = ('\n'.join(contents))    
    return result
total=len(fileNames)
done=0;
for f in fileNames:
    print "Done :"+ str(done) + "Remaning : "+ str(total)
    done=done+1;
    total=total-1;
    dic={}
    dic={}
    username=f;
    url = "http://www.codechef.com/users/"+username;
    link=url
    c.execute("SELECT * FROM users  WHERE url = ?", (link,))
    data=c.fetchone()
    try:
        if data is None:
            print('Adding user with link %s'%link)
            sys.stdout.flush()
            dic['url']=link.strip()
            try:
                #page = urllib2.urlopen(url).read()
                page=readFile('users/'+f);
            except:
                continue;
            soup=BeautifulSoup(page)
            tablerating= soup.find("table",{"class":"rating-table"})
            table2=tablerating.find_all("tr")
            longrow=table2[1].find_all("td")[2].get_text()
            longrow=longrow[:-8]
            shortrow=table2[2].find_all("td")[2].get_text()
            shortrow=shortrow[:-8]
            dic['long_rating']=float(longrow)
            dic['short_rating']=float(shortrow)
            hx=soup.findAll("hx")
            try:
                dic['long_global_rank']=int(hx[0].get_text())
            except:
                dic['long_global_rank']=-1;
            try:
                dic['long_country_rank']=int(hx[1].get_text())
            except:
                dic['long_country_rank']=-1;
            try:
                dic['short_global_rank']=int(hx[2].get_text())
            except:
                dic['short_global_rank']=-1
            try:
                dic['short_country_rank']=int(hx[3].get_text())
            except:
                dic['short_country_rank']=-1
            table1= soup.find("div",{"class":"profile"}).findAll("table",{"border":"0"})[1]
            table2=table1.find_all("tr")
            table2=table2[:10]
            for row in table2:
                cells=row.find_all("td")
                field=cells[0].get_text()
                field=field[:-1]
                field=field.lower();
                val=cells[1].get_text()
                if field=="student/professional":
                    field="student_professional"
                if field=="about me":
                    field="about_me"
                if field=="organisation" or field=="institution":
                    field="institution"
                dic[field]=val.strip()
                #print field
                #print val
                #print cells
            #print dic
            try:
                c.execute('''insert into users values
                         (:username,
                         :name,
                         :url,
                        :long_rating,
                        :short_rating,
                        :long_global_rank,
                        :long_country_rank,
                        :short_global_rank,
                        :short_country_rank,
                        :country,
                        :state,
                        :city,
                        :motto,
                        :link,
                        :about_me,
                        :student_professional,
                        :institution
                         )''',dic)
                #db.commit()
                print "successfully added "+dic['username'];
            except:
                print "error occured while adding  "+dic['username']
        else:
            print('Already added link %s'%link)
    except:
        print "error"#because maybe invalid page or url with spaces
    if total%100==0:
        db.commit()
    sys.stdout.flush()
db.commit()
db.close()
