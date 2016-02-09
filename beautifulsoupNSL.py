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
teachersCsv = 'cache/faculty-education.csv'   #variables for files. same folder for ease.

def findli(type):
    if not temped[tempvar].get_text().find(type) == -1:
        empty[2] = type
        empty[3] = temped[tempvar].get_text().replace('\xa0', '').split(', ')[1].split('\n')[0]
                        
def findp(type):
    if not temped[tempvar].find(type) == -1:
        empty[2] = type
        empty[3] = temped[tempvar].replace('\xa0', '').split(', ')[1]
        
        
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
    header = ["Name", "Rank", "Degree", "Institution"]
    print("Creating teachers.csv to store data")
    with open(teachersCsv, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
else: 
    print("recreating teachers.csv...")
    os.remove(teachersCsv)
    header = ["Name", "Rank", "Degree", "Institution"]
    print("Creating teachers.csv to store data")
    with open(teachersCsv, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
    

#Here's where the "Fun" begins

while countdep < depcount:
    profcount = len(modefind.find_all('ul')[countdep].find_all('li'))
        #finding out how many professors are in the current department
    countprof = 0
        #resetting the current professor count for each department
    while countprof < profcount:
        empty = ["", "", "", ""]
        rowcount = 0
            #splits name and rank into a tuple, used variable to slim down for next two
        
        if len(modefind.find_all('ul')[countdep].find_all('li')[countprof].find_all('a')) > 0:
            #if length of websites is greater than 0 (has a website)
            empref = modefind.find_all('ul')[countdep].find_all('a')[countprof].get('href')
            #find the href and set to empref
            if empref.startswith('http://www.suffolk.edu'): #just in case it starts with prefix
                empref = empref.split('http://www.suffolk.edu')[1] #get the current website
                        #About to get full of bullshit code right here...
            tempdata = urllib.request.urlopen("http://www.suffolk.edu" + empref).read().decode("utf-8")
            tempdata = tempdata.replace(u'\u2013', u'-')
            tempdata = tempdata.replace(u'\xa0', u' ')
            tempdata = tempdata.replace(u'\u2019', u"\'")
                #set current web address to tempdata
            temploc = tempdata.find('3>Education') 
            #set temp location to shorten soup            
            tempdata2 = tempdata[temploc:]
            tempsoup = BeautifulSoup.BeautifulSoup(tempdata[temploc:temploc+250], 'lxml')
            if len(tempsoup.find_all('h3')) > 0:
                temploc2 = tempdata2.find('<h3')
            else:
                if len(tempsoup.find_all('ul')) > 0:
                    temploc2 = tempdata2.find('/ul>')+5
                else:
                    temploc2 = tempdata2.find('/p>')+4
            tempdata2 = tempdata2[:temploc2]
            tempsoup = BeautifulSoup.BeautifulSoup(tempdata2, 'lxml')
                #temp beautifulSoup
            if not len(tempsoup.find_all('li')) == 0:
                temped = tempsoup.find_all('li')
                templi = 1
            else:
                if temploc == -1:
                    temped = tempsoup
                if temploc > 0:
                    temped = tempsoup.find_all('p')[1].get_text().split('\n ')
                templi = 0
            templen = len(temped)
            tempvar = 0
                    
            while tempvar < templen:
                if templi == 1:
                    name = modefind.find_all('ul')[countdep].find_all('li')[countprof].get_text().split(', ')
                    empty[0] = name[0]
                    empty[1] = name[1]
                    empty[2] = ''
                    empty[3] = ''
                    findli('PhD')
                    findli('MS')
                    findli('BS')
                    if not empty[2] == '':
                        with open(teachersCsv, 'a', newline='') as csvfile:
                        #'a' to append instead of overwrite the first line each time
                            writer = csv.writer(csvfile)
                            writer.writerow(empty)
                        rowcount += 1
                    if empty[2] == '' and (tempvar+1) == templen and rowcount == 0:
                        with open(teachersCsv, 'a', newline='') as csvfile:
                        #'a' to append instead of overwrite the first line each time
                            writer = csv.writer(csvfile)
                            writer.writerow(empty)
                    tempvar += 1
                if templi == 0:
                    name = modefind.find_all('ul')[countdep].find_all('li')[countprof].get_text().split(', ')
                    empty[0] = name[0]
                    empty[1] = name[1]
                    empty[2] = ''
                    empty[3] = ''
                    findp('PhD')
                    findp('MS')
                    findp('BS')
                    if not empty[2] == '':
                        with open(teachersCsv, 'a', newline='') as csvfile:
                        #'a' to append instead of overwrite the first line each time
                            writer = csv.writer(csvfile)
                            writer.writerow(empty)
                        rowcount += 1
                    if empty[2] == '' and (tempvar+1) == templen:
                        with open(teachersCsv, 'a', newline='') as csvfile:
                        #'a' to append instead of overwrite the first line each time
                            writer = csv.writer(csvfile)
                            writer.writerow(empty)
                    tempvar += 1
        else:
            name = modefind.find_all('ul')[countdep].find_all('li')[countprof].get_text().split(', ')
            empty[0] = name[0]
            empty[1] = name[1]
            with open(teachersCsv, 'a', newline='') as csvfile:
                            #'a' to append instead of overwrite the first line each time
                writer = csv.writer(csvfile)
                writer.writerow(empty)
        countprof += 1
        
    countdep += 1
    #move to next department until finished with all departments

