from bs4 import BeautifulSoup
import urllib
import urllib2
import json
import sqlite3
import sys

db=sqlite3.connect('codechef.db')
c=db.cursor()
links=[]
f=open("links.txt","w")
for link in c.execute('select * from links'):
    f.write(link[0]+"\n")
    links.append(link[0])
#print links
f.close()
db.close()
