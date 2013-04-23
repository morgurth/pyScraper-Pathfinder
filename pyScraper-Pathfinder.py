#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
from HTMLParser import HTMLParser
import urllib2
import re
import numpy

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def write_weapons(weapons_table):
    print "Creating the Weapons Table input file: ",

    f = open("weaponstable.txt", "w")

    f.write("WEAPONS\n")
    f.write("Name;Cost;Damage;Critical;Range;Weight;Type;Special\n")

    f.write(weapons_table[0] + ";" + weapons_table[1] + "\n")

    newrow = False

    for count in range(11,len(weapons_table)):
        if not newrow:
            f.write(weapons_table[count] + ";")
  
    f.close
    
    print "[\033[92m OK \033[0m]"
    return

html = urllib2.urlopen('http://www.d20pfsrd.com/equipment---final/weapons')
pagesource = html.read()

soup = BeautifulSoup(pagesource)

alltables = soup.findAll( "table", { "style":"border-color:rgb(136,136,136);border-width:1px;border-collapse:collapse;margin:5px 0px;width:100%" } )

results = []

for table in alltables:
    rows = table.findChildren(['th', 'tr'])
    weapon_line = []
    weapon_list = []
    header_line = []
    header_list = []

    for th in rows:
        header = th.findChildren('th')

        for th in header:
            text = th.renderContents().strip('\n')
            text = strip_tags(text)
            text = text.translate(None, '12')
            header_line.append(text)

    header_list = ';'.join(header_line)
    header_list = re.split(';|\n', header_list)
    header_list[0] = header_list[0].translate(None, '()')
    
    results.append(header_list)

    for tr in rows:
        cols = tr.findAll('td')
        for td in cols:
            text = td.renderContents().strip('\n')
            text = strip_tags(text)
            weapon_line.append(text)

    weapon_list = ';'.join(weapon_line)
    weapon_list = weapon_list.split(';')
    items, chunk = weapon_list, 10
    temp_weapon_table = zip(*[iter(items)]*chunk)

    results.append(temp_weapon_table)

for result in results:
    print(result)

#result_list = results[0].split('\n')

#result_list[0] = strip_tags(result_list[0].translate(None, '()')) 

#write_weapons(result_list)
