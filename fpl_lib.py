# -*- coding: utf-8 -*-
"""
Created on Mon May 31 15:59:41 2021

@author: Eric Buehler
"""


class token:
    def __init__(self, name):
        self.token = name
        
class constant:
    def __init__(self, name):
        self.token = name
        
        
class commandtoken(token):
    pass

class text(constant):
    pass
      
class quotetoken(token):
    pass

class whitespace(constant):
    pass

class openparenthesistoken(token):
    pass

class closeparenthesistoken(token):
    pass

class commatoken(token):
    pass

class equaltoken(token):
    pass

class newlinetoken(token):
    pass

class openbrackettoken(token):
    pass

class closebrackettoken(token):
    pass


        
class tokenizer:
    def __init__(self, program, commands):
        self.program=program.strip()
        self.program+="\n "
        self.program_raw=program.strip()
        self.cmdprogram=commands
        

    def tokenize(self):
        self.tokens=[]
        self.tabs=[]
        
        self.program_lines=self.program_raw.split("\n")

        for self._i in range(0,self.program.count("\n")):
            self._line = self.program_lines[self._i]
            
            if self._line.isspace() or self._line=="":
                continue
            
                   
            if len(self._line)>0 and self._line.strip()[0]=="#":
                self._i+=1
                continue
            
                        
            self.line=self._line
            self._line=self._line.strip()
            
    
    

            self._n=0
            while self._n<len(self.cmdprogram):
                if self._line.find(self.cmdprogram[self._n],0,len(self._line))==0:
                    varflag=False
                    break
                self._n+=1
                if self._n==len(self.cmdprogram):
                    varflag=True
                    break
            
            if varflag:
                    pass
            if not varflag:
                self.tokens.append(commandtoken(self._line[0:len(self.cmdprogram[self._n])]))
                


            if varflag:
                self.tab_pos=0
                for _ in range(len(self._line)):
                    if not self._line[self.tab_pos].isspace():
                        break
                    
                    self.tab_pos+=1
                    
                        
            if not varflag:
                self.tab_pos=self.line.find(self.cmdprogram[self._n],0,len(self.line))+1
                
            self.tabs.append(self.line[0:self.tab_pos-1].count("    "))
            
                
            
            if varflag:
                self.lastpos=0
            if not varflag:
                self.lastpos=len(self.cmdprogram[self._n])
                
                
            while self.lastpos<len(self._line):
                self._char=self._line[self.lastpos]
                
                if self._char=='"':
                    self.tokens.append(quotetoken('"'))
                    
                elif self._char=="(":
                    self.tokens.append(openparenthesistoken('('))
                    
                elif self._char==")":
                    self.tokens.append(closeparenthesistoken(')'))
                    
                elif self._char==",":
                    self.tokens.append(commatoken(','))
                    
                elif self._char=="=":
                    self.tokens.append(equaltoken('='))
                    
                elif self._char=="[":
                    self.tokens.append(openbrackettoken('['))
                    
                elif self._char=="]":
                    self.tokens.append(closebrackettoken(']'))

                elif self._char.isspace():
                    self.tokens.append(whitespace(self._char))
                    self.lastpos+=1
                    continue
                
                else:
                    self.tokens.append(text(self._line[self.lastpos]))
                    
                self.lastpos+=1
                
            self.tokens.append(newlinetoken('\n'))

        return self.tokens

            

class quotedata:
    def __init__(self, quotes, tokens):
        self.quotes=quotes        
        self.tokens=tokens
        
    def get(self):
        self.text=[]

        for n in range(self.quotes[0]+1,self.quotes[len(self.quotes)-1]):
            self.text.append(self.tokens[n].token)

        return "".join(self.text).replace("\\n", "\n").replace("\\t", "\t")