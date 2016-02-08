# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 16:46:00 2016

@author: butticorn
"""
import os.path
import bs4 as BeautifulSoup
import urllib.request
url6578 = 'cache/suffolk6578.php'

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