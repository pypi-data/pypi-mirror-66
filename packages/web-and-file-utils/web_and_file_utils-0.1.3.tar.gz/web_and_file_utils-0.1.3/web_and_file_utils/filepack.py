# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 20:01:36 2020

@author: shriy
"""
import os
import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def get_files_list(fpath,ext):
    files_found=[]
    for i in fpath:
        for r, d, f in os.walk(i):
            for item in f:
                if item.endswith('.'+ext):
                    files_found.append(os.path.join(r,item))
    with open('filelist.txt','w') as myfile:
        for items in files_found:
            myfile.write('%s\n' % items)
            
def mail_files_list(path,ext,fromadd,toadd,pswd,smtphost):
    files_found=[]
    for i in path:
        for r, d, f in os.walk(i):
            for item in f:
                if item.endswith('.'+ext):
                    files_found.append(os.path.join(r,item))
    with open('filelist.txt','w') as myfile:
        for items in files_found:
            myfile.write('%s\n' % items)
    currpath = os.getcwd()
    currpath1 = currpath
    completepath = os.path.join(currpath1,"filelist.txt")
    fromaddress = fromadd
    toaddress = toadd
    msg = MIMEMultipart()    
    msg['From'] = fromaddress
    msg['To'] = toaddress
    msg['Subject'] = "Files List Result" 
    body = "Here is the result"
    msg.attach(MIMEText(body, 'plain')) 
    filename = "filelist.txt"
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
    
