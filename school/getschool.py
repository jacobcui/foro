from time import sleep
from copy import copy
from string import find
from HTMLParser import HTMLParser, HTMLParseError

import django

from django.db import models
from school.models import School
import json, requests

from school.helper import SchoolHelper

url = 'http://house.ksou.cn/topschool.php'

params = dict(
    sta = "nsw",
)

def getschool(url, params):
    err = 0
    try:
        resp = requests.get(url=url, params=params)
    except ConnectionError as e:
        print e
        err = 1
    except HTTPError as e:
        print e
        err = 2

    if err > 0:
        print err
        return []
    
    html = resp.text

    if find(html, "Your request is under process") > 0:
        return -1
#html = '<table cellspacing=0 cellpadding=5 width=100% style="font-size:13px"><tr height=25 bgcolor="#E7EBFF" style="font-size:14px"><td>&nbsp;<b>Rank</b></td><td><b>School Name</b></td><td><b>Suburb</b></td><td><b>Score</b></td></tr><tr height=20><td>&nbsp;2</td><td><a href="school.php?id=1982">Balmain Public School</a></td><td><a href="result_school.php?sta=nsw&q=Balmain">Balmain</a></td><td>&nbsp;608</td></tr><tr height=20 bgcolor="#F4F4F4"><td>&nbsp;3</td><td><a href="school.php?id=1957">Woollahra Public School</a></td><td><a href="result_school.php?sta=nsw&q=Woollahra">Woollahra</a></td><td>&nbsp;602</td></tr><tr height=20><td>&nbsp;4</td><td><a href="school.php?id=1952">Artarmon Public School</a></td><td><a href="result_school.php?sta=nsw&q=Artarmon">Artarmon</a></td><td>&nbsp;600</td></tr><tr height=20 bgcolor="#F4F4F4"><td>&nbsp;5</td><td><a href="school.php?id=1979">Neutral Bay Public School</a></td><td><a href="result_school.php?sta=nsw&q=Neutral+Bay">Neutral Bay</a></td><td>&nbsp;599</td></tr><tr height=20><td>&nbsp;7</td><td><a href="school.php?id=1974">Summer Hill Public School</a></td><td><a href="result_school.php?sta=nsw&q=Summer+Hill">Summer Hill</a></td><td>&nbsp;588</td></tr><tr height=20 bgcolor="#F4F4F4"><td>&nbsp;8</td><td><a href="school.php?id=2053">Erskineville Public School</a></td><td><a href="result_school.php?sta=nsw&q=Erskineville">Erskineville</a></td><td>&nbsp;585</td></tr><tr height=20><td>&nbsp;10</td><td><a href="school.php?id=2113">Ermington Public School</a></td><td><a href="result_school.php?sta=nsw&q=West+Ryde">West Ryde</a></td><td>&nbsp;581</td></tr><tr height=20 bgcolor="#F4F4F4"><td>&nbsp;12</td><td><a href="school.php?id=1985">Matthew Pearce Public School</a></td><td><a href="result_school.php?sta=nsw&q=Baulkham+Hills">Baulkham Hills</a></td><td>&nbsp;576</td></tr><tr height=20><td>&nbsp;16</td><td><a href="school.php?id=2035">Chatswood Public School</a></td><td><a href="result_school.php?sta=nsw&q=Chatswood">Chatswood</a></td><td>&nbsp;574</td></tr><tr height=20 bgcolor="#F4F4F4"><td>&nbsp;17</td><td><a href="school.php?id=12312">Waitara Public School</a></td><td><a href="result_school.php?sta=nsw&q=Wahroonga">Wahroonga</a></td><td>&nbsp;573</td></tr><tr height=20><td>&nbsp;18</td><td><a href="school.php?id=1993">Beecroft Public School</a></td><td><a href="result_school.php?sta=nsw&q=Beecroft">Beecroft</a></td><td>&nbsp;571</td></tr>'

    schools = []

    class MyHTMLParser(HTMLParser):
        idx = 0
        node = dict()
        def handle_starttag(self, tag, attrs):
            node = self.node
            if tag == "tr":
                self.idx = 0
            elif tag == "td":
                self.idx = self.idx + 1
            elif tag == "a":
                if (len(attrs[0])) > 1:
                    if find(attrs[0][1], "id=") > 0 :
                        if self.idx == 3:
                            node['link'] = attrs[0][1]
                            return
            elif tag == "script":
                return
                        
        def handle_endtag(self, tag):
            return
    
        def handle_data(self, data):
            node = self.node
            #print data, " ", self.idx
            if self.idx == 1:
                node['suburb'] = data
            elif self.idx == 2:
                node['type'] = data
            elif self.idx == 3:
                node['name'] = data
            elif self.idx == 4:
                node['rank'] = data
                schools.append(copy(node))
            return

    parser = MyHTMLParser()
    parser.feed(html)

    for school in schools:
        print school
    quit()
    return copy(schools)

def getaddress(school):
    url = 'http://house.ksou.cn/' + school['link']
#    print "\n"
#    print url
    err = 0
    try:
        resp = requests.get(url)
    except ConnectionError as e:
        print e
        err = 1
    except HTTPError as e:
        print e
        err = 2
    except requests.exceptions.RequestException as e:
        print e
        err = 5
    if err > 0:
        print err
        return []

    html = resp.text
    if find(html, "Your request is under process") > 0:
        return -1

#    html = '<table cellspacing="0" cellpadding="0" style="font-size:13px" width="100%"><tbody><tr height="20"><td width="150"><b>School sector:</b></td><td>Government</td></tr><tr height="20"><td width="150"><b>School type:</b></td><td>Primary school</td></tr><tr height="20"><td width="150"><b>Gender:</b></td><td>Co-Ed</td></tr><tr height="20"><td><b>Total student:</b></td><td>193&nbsp;(boy:108, girl:85)</td></tr><tr height="20"><td><b>Total staff:</b></td><td>9</td></tr><tr height="20"><td><b>Student attendance:</b></td><td><table cellspacing="0" cellpadding="0"><tbody><tr valign="center"><td>97%</td><td><a href="#" onclick="showHelp(1);return false" title="What is student attendance rate?"><img border="0" src="/img/question.jpg"></a></td></tr></tbody></table></td></tr><tr height="20"><td><b>None-english student:</b></td><td><table cellspacing="0" cellpadding="0"><tbody><tr valign="center"><td>56%</td><td><a href="#" onclick="showHelp(3);return false" title="What is None-english student?"><img border="0" src="/img/question.jpg"></a></td></tr></tbody></table></td></tr><tr height="20" valign="center"><td><b>ICSEA value:</b></td><td><table cellspacing="0" cellpadding="0"><tbody><tr valign="center"><td>1163, ranks No.174 <a href="topschool.php?type=3&amp;sta=nsw">More ICSEA Ranking...</a></td><td><a href="#" onclick="showHelp(2);return false" title="What is ICSEA?"><img border="0" src="/img/question.jpg"></a></td></tr></tbody></table></td></tr><tr height="20" valign="center"><td><b>ICSEA distribution:</b></td><td><table cellpadding="2" cellspacing="0" border="1"><tbody><tr><td align="center">Bottom quarter</td><td colspan="2" align="center">Middle quarters</td><td align="center">Top quarter</td></tr><tr><td align="center">4%</td><td align="center">2%</td><td align="center">33%</td><td align="center">61%</td></tr></tbody></table></td></tr><tr height="20"><td><b>Website:</b></td><td><a href="http://www.balmain-p.schools.nsw.edu.au" target="_blank">http://www.balmain-p.schools.nsw.edu.au</a></td></tr><tr height="20"><td><b>Location:</b></td><td><a href="http://house.ksou.cn/profile.php?sta=nsw&amp;q=Balmain">Balmain</a></td></tr><tr height="40" valign="top"><td><b>Address:</b></td><td>Balmain Public School, BALMAIN NSW 2041<br><a href="http://house.ksou.cn/p.php?sta=nsw&amp;q=Balmain+Public+School%2C+BALMAIN+NSW+2041">Nearby House Price</a>&nbsp;&nbsp;<a href="http://house.ksou.cn/rp.php?sta=nsw&amp;q=Balmain+Public+School%2C+BALMAIN+NSW+2041">Nearby House Rent</a></td></tr><tr height="20"><td><b>Phone:</b></td><td>02 9818 1177</td></tr></tbody></table>'

    address = dict()
    class MyHTMLParser(HTMLParser):
        idx = 0
        node = dict()
        addressline = False
        onlyaddressline = False
        def handle_starttag(self, tag, attrs):
            node = self.node
            if tag == "tr":
                self.idx = 0
                self.addressline = False
            elif tag == "td":
                self.idx = self.idx + 1
            elif tag == "script":
                return
        def handle_endtag(self, tag):
            return
    
        def handle_data(self, data):
            if data == "Address:":
                self.addressline = True
                self.onlyaddressline = True
            if self.onlyaddressline and self.addressline == True and self.idx == 2:  
                address['address'] =  data
                self.onlyaddressline = False
            return
    try:
        parser = MyHTMLParser()
        html = html.replace("n<reviews", "")
        html = html.replace("&", "and")
        html = html.replace(
            "document.getElementById(\"head_new\").innerHTML='<a href=\"newhome.php?q='+region+\", \"+state.toUpperCase()+'\">New Home</a>'", "");
        parser.feed(html)
    except HTMLParseError as e:
        print e
        address = dict()
        quit()
    return copy(address)

schools = -1
while (schools < 0):
    schools = getschool(url, params)
    if(schools < 0):
        sleep(30)
        continue

i = 10000

helper = SchoolHelper()

for school in  schools:
    try:
        if helper.doesExists(school['name']):
            print school['name'], " was stored already, now ignored."
            continue

        res = -1
        while res < 0:
            res = getaddress(school)
            sleep(5)
            if res < 0:
                sleep(20)
                continue
            else:
                school['address'] = res['address']

        print school    
        s = School(
            name= school['name'],
            rank= school['rank'],
            suburb= school['suburb'],
            score= school['score'],
            link= school['link'],
            address= school['address']
            )
        s.save()

    except KeyError as e:
        print e
    
    i = i - 1
    if i <= 0:
            break
    
