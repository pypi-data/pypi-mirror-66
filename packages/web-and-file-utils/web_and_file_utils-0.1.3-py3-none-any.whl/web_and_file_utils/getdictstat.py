# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 20:48:06 2020

@author: shriy
"""

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import os
import os.path

def urldictstat_with_dirpath(directory_path):
    location = directory_path
    files_found = []
    for r, d, f in os.walk(location):
        for item in f:
            if '.url' in item:
                files_found.append(os.path.join(r,item))
    diction = []
    for item in files_found:
        with open(item, "r") as myfiles:
            for line in myfiles:
                if (line.startswith('URL')):
                    url = line[4:]
                    break
        diction.append(url);
    with open('output.txt', 'w') as myfile:
        for items in diction:
            myfile.write('%s' % items)
    currpath = os.getcwd()
    currpath1 = currpath
    completepath = os.path.join(currpath1,"output.txt") 
    f = open(completepath,"r")
    f1 = f.read().split()       
    dic={}
    for x in f1:
        req = Request(x)
        try:
            response = urlopen(req)
        except HTTPError as e:
            dic[x]='Error code: '+str(e.code)
        except URLError as e:
            dic[x]='Failed to reach server, Reason: '+str(e.reason)
        else:
            dic[x]='Status OK'
    f.close()
    return dic

def urldictstat_with_file(filepath):
    f = open(filepath,"r")
    f1 = f.read().split()
    dic={}
    for x in f1:
        req = Request(x)
        try:
            response = urlopen(req)
        except HTTPError as e:
            dic[x]='Error code: '+str(e.code)
        except URLError as e:
            dic[x]='Failed to reach server, Reason: '+str(e.reason)
        else:
            dic[x]='Status OK'
    f.close()
    return dic


