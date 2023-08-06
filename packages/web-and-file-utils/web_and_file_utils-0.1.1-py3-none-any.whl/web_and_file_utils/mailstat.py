# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 19:57:04 2020

@author: shriy
"""
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import os
import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def urlstatmail_with_dirpath(directory_path,fromadd,toadd,pswd,smtphost):
    location = directory_path
    files_found = []
    for r, d, f in os.walk(location):
        for item in f:
            if '.url' in item:
                files_found.append(os.path.join(r,item))
    diction = []
    for item in files_found:
        with open(item, "r") as myfile:
            for line in myfile:
                if (line.startswith('URL')):
                    url = line[4:]
                    break
        diction.append(url);
    with open('output.txt', 'w') as myfiles:
        for items in diction:
            myfiles.write('%s' % items)
    currpath = os.getcwd()
    currpath1 = currpath
    completepath = os.path.join(currpath1,"output.txt") 
    f = open(completepath,"r")
    f1 = f.read().split()
    currpath2 = os.getcwd()
    currpath3 = currpath2
    completepath1 = os.path.join(currpath3,"res.txt")        
    f2 = open(completepath1,"w")
    for x in f1:
        req = Request(x)
        try:
            response = urlopen(req)
        except HTTPError as e:
            f2.write("\n"+x)
            f2.write('\nServer could not fulfill request')
            f2.write('\nError code: '+ str(e.code)+"\n")
        except URLError as e:
            f2.write("\n"+x)
            f2.write('\nFailed to reach server')
            f2.write('\nReason: '+str( e.reason)+"\n")
        else:
            f2.write("\n"+x)
            f2.write('\nStatus OK\n')
    f2.close()
    f.close()
    fromaddress = fromadd
    toaddress = toadd
    msg = MIMEMultipart()    
    msg['From'] = fromaddress
    msg['To'] = toaddress
    msg['Subject'] = "URL Status Alert" 
    body = "Here is the result"
    msg.attach(MIMEText(body, 'plain')) 
    filename = "res.txt"
    attachment = open(completepath1, "rb") 
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read()) 
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    msg.attach(p) 
    s = smtplib.SMTP(smtphost, 587)  
    s.starttls() 
    s.login(fromaddress,pswd) 
    text = msg.as_string() 
    s.sendmail(fromaddress, toaddress, text) 
    s.quit() 

def urlstatmail_with_file(filepath,fromadd,toadd,pswd,smtphost):
    f = open(filepath,"r")
    f1 = f.read().split()
    currpath = os.getcwd()
    currpath1 = currpath
    completepath = os.path.join(currpath1,"res.txt")        
    f2 = open(completepath,"w")
    for x in f1:
        req = Request(x)
        try:
            response = urlopen(req)
        except HTTPError as e:
            f2.write("\n"+x)
            f2.write('\nServer could not fulfill request')
            f2.write('\nError code: '+ str(e.code)+"\n")
        except URLError as e:
            f2.write("\n"+x)
            f2.write('\nFailed to reach server')
            f2.write('\nReason: '+str( e.reason)+"\n")
        else:
            f2.write("\n"+x)
            f2.write('\nStatus OK\n')
    f2.close()
    f.close()
    fromaddress = fromadd
    toaddress = toadd
    msg = MIMEMultipart()    
    msg['From'] = fromaddress
    msg['To'] = toaddress
    msg['Subject'] = "URL Status Alert" 
    body = "Here is the result"
    msg.attach(MIMEText(body, 'plain')) 
    filename = "res.txt"
    attachment = open(completepath, "rb") 
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read()) 
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    msg.attach(p) 
    s = smtplib.SMTP(smtphost, 587)  
    s.starttls() 
    s.login(fromaddress,pswd) 
    text = msg.as_string() 
    s.sendmail(fromaddress, toaddress, text) 
    s.quit()
    