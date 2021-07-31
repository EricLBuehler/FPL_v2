# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 18:15:42 2021

@author: Eric Buehler
"""

fpl_lib=open("fpl_lib.py", "r")
fpl_loader=open("fpl_loader.py", "r")
fpl_main=open("fpl_main.py", "r")

text_all=fpl_lib.read()+fpl_loader.read()+fpl_main.read()

fpl_lib.close()
fpl_loader.close()
fpl_main.close()

fpl_lib=open("fpl_lib.py", "r")
fpl_loader=open("fpl_loader.py", "r")
fpl_main=open("fpl_main.py", "r")

text_fpl_lib=fpl_lib.read()
text_fpl_loader=fpl_loader.read()
text_fpl_main=fpl_main.read()

fpl_lib.close()
fpl_loader.close()
fpl_main.close()

text_all=text_all.split("\n")
text_fpl_lib=text_fpl_lib.split("\n")
text_fpl_loader=text_fpl_loader.split("\n")
text_fpl_main=text_fpl_main.split("\n")

lines_all=0
lines_fpl_lib=0
lines_fpl_loader=0
lines_fpl_main=0

for line in text_all:
    if line.isspace():
        continue
    
    lines_all+=1
    
    
for line in text_fpl_lib:
    if line.isspace():
        continue
    
    lines_fpl_lib+=1
    
for line in text_fpl_loader:
    if line.isspace():
        continue
    
    lines_fpl_loader+=1
    
for line in text_fpl_main:
    if line.isspace():
        continue
    
    lines_fpl_main+=1
    
print("Total lines of code in project: "+str(lines_all))
print("fpl_main.py lines of code: "+str(lines_fpl_main))
print("fpl_lib.py lines of code: "+str(lines_fpl_lib))
print("fpl_loader.py lines of code: "+str(lines_fpl_loader))