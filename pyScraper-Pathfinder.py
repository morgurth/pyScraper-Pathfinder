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

    for count in range(0,len(weapons_table)):
        if count%2==0:
           f.write(weapons_table[count][0] + ';' + weapons_table[count][1] + '\n')
        else:
           for result in weapons_table[count]:
               f.write(result[0] + ';' + result[1] + ';' + result[3] + ';' + result[4] + ';' + result[5] + ';' + result[6] + ';' + result[7] + '\n')

    f.close
    
    print "[\033[92m OK \033[0m]"
    return

def weapons_parse(source): 
    html = urllib2.urlopen(source)
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
                text = strip_tags(text.lstrip())
                weapon_line.append(text)

        weapon_list = ';'.join(weapon_line)
        weapon_list = weapon_list.split(';')

        items, chunk = weapon_list, 10
        temp_weapon_table = zip(*[iter(items)]*chunk)

        results.append(temp_weapon_table)

    return results

weapon_result_list = weapons_parse('http://www.d20pfsrd.com/equipment---final/weapons')

write_weapons(weapon_result_list)
