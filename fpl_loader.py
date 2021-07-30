# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 18:38:15 2021

@author: Eric Buehler
"""

class loader:
    def __init__(self, filename):
        self.file=open(filename,"r")
    
    def load(self):
        self.raw=self.file.read()
        self.file.close()
        
        return self.raw
