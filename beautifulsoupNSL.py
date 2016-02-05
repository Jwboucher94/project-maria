# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 16:46:00 2016

@author: butticorn
"""
import os.path
import bs4 as BeautifulSoup
import urllib.request

if not os.path.isfile("cache/networksciencelab.com.html"):
    print("Attempting to cashing the data...")
    if not os.path.isdir("cache"):
        os.mkdir("cache")
    data = urllib.request.urlopen("http://networksciencelab.com/").read().decode("utf-8")
    outfile = open("cache/networksciencelab.com.txt", "w")
    outfile.write(data)
    outfile.close()

with open("cache/networksciencelab.com.html") as infile:
    soup = BeautifulSoup.BeautifulSoup(infile)