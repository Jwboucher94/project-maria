# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 16:46:00 2016

@author: butticorn
"""
import os.path
import bs4 as BeautifulSoup     #import statements...
import urllib.request
import csv

url6578 = 'cache/suffolk6578.php'
teachersCsv = 'cache/teachers.csv'   #variables for files. same folder for ease.

if not os.path.isfile(url6578):
    print("Attempting to cashing the data...")
    if not os.path.isdir("cache"):
        os.mkdir("cache")
    data = urllib.request.urlopen("http://www.suffolk.edu/college/6578.php").read().decode("utf-8")
    data = data.replace(u'\u2013', u'-')
    data = data.replace(u'\xa0', u' ')
    data = data.replace(u'\u2019', u"\'")
    outfile = open(url6578, "w")
    outfile.write(data)
    outfile.close()

with open(url6578) as infile:
    soup = BeautifulSoup.BeautifulSoup(infile, 'lxml')

modefind = soup.find('ul', { "class" : "mod-showhide" })
depcount = len(modefind.find_all('h2'))+1 #department count
countdep = 0
if not os.path.isfile(teachersCsv): #create the teachers.csv file, if not already created
    header = ["Name", "Rank", "MS", "BS", "PhD", "Institute"]
    print("Creating teachers.csv to store data")
    with open(teachersCsv, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
else: 
    print("teachers.csv exists... was this okay with you? Appending to current file...")
while countdep < depcount:
    #do stuff here?
    profcount = len(modefind.find_all('ul')[countdep].find_all('li'))
        #finding out how many professors are in the current department
    countprof = 0
        #resetting the current professor count for each department
    while countprof < profcount:
        #do stuff here too
        empty = ["", "", "", "", "", ""]
        if countdep > 11: #because of second ul in psych, had to compensate.
            empty[5] = modefind.find_all('h2')[countdep-1].get_text()
        else:
            empty[5] = modefind.find_all('h2')[countdep].get_text()
        name = modefind.find_all('ul')[countdep].find_all('li')[countprof].get_text().split(', ')
            #splits name and rank into a tuple, used variable to slim down for next two
        #ms bs phd here
        
        if len(modefind.find_all('ul')[countdep].find_all('li')[countprof].find_all('a')) > 0:
            emp = modefind.find_all('ul')[countdep].find_all('a')[countprof].get('href')
            if emp.startswith('http://www.suffolk.edu'):
                emp = emp.split('http://www.suffolk.edu')[1] #get the current website
           
           
          #finish ms bs phd
        else:
            empty[2] = ''
        empty[0] = name[0]
        empty[1] = name[1]
        with open(teachersCsv, 'a', newline='') as csvfile:
                #'a' to append instead of overwrite the first line each time
            writer = csv.writer(csvfile)
            writer.writerow(empty)
        countprof += 1
        #move to next professor until finished with that section
    countdep += 1
    #move to next department until finished with all departments


    #   Trouble trying to find how to get the MS, BS, and PhD. Partial string search possible?
    #   11 and 12 ul under psych, had to compensate as such.
    #   modefind.find_all('h2')[0].get_text() to get first Department name
    #   temporarily, can get a tuple with name and rank using this line:
    #   modefind.find_all('ul')[countdep].find_all('li')[countprof].get_text().split(', ')