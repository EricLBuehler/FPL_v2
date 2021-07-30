# -*- coding: utf-8 -*-
"""
Created on Mon May 31 16:00:22 2021

@author: Eric Buehler
"""

import fpl_lib
import fpl_loader
import time

class fpl_env:
    def __init__(self):
        self.envvars={}
    
    def eval_fpl(self, string):
        return eval(string, self.envvars)
    
    def exec_fpl(self, string):
        return exec(string, self.envvars)


def fpl_exec_tokenized(tokens, tabs, commands, evalfpl): 
    commands_origin=commands
    inloop={"wasinloop":False, "inloop":False, "looptype":"", "lastline":0, "firstline":0} 
    functions={}
    
    
    #Split lines
    
        
    lines=[]
    index=0
    for token in tokens:
        if isinstance(token, fpl_lib.newlinetoken):
            lines.append([])
            
        index+=1
        


    index2=0
    for n in range(index):
        token=tokens[n]
        
        if isinstance(token, fpl_lib.newlinetoken):
            index2+=1
        
        if not isinstance(token, fpl_lib.newlinetoken):
            lines[index2].append(token)
            
            

    #assert len(tabs)==len(lines) #!!!!!!!!!!!!!!!!!!!!!!!        

    lineindex=0
    while True:
        line=lines[lineindex]
        tablevel=tabs[lineindex]

          
   
        #Get command/parenthesis
        commands=[]
        parenthesis=[]
        
        index=0
        for token in line:
            if isinstance(token,fpl_lib.commandtoken):
                commands.append(token.token)
                index+=1
                continue
    
            if isinstance(token,fpl_lib.openparenthesistoken) or isinstance(token,fpl_lib.closeparenthesistoken):
                parenthesis.append(index)
        
            index+=1
        
           
        #no command, must be a variable operation/function operation
        if len(commands)==0: 
            funcnames=[]
            for item in functions:
                funcnames.append(item)
                
                
            #Get equal signs
            equals=[]
            index=0
            for token in line:
                if isinstance(token, fpl_lib.equaltoken):
                    equals.append(index)
                    
                index+=1
                
            vartokens_=[]
            for vartoken in line:
                vartokens_.append(vartoken.token)
                
            vartokens="".join(vartokens_)
            

            #Function
            if vartokens[0:vartokens.find("(")] in funcnames:
                funcname=vartokens[0:vartokens.find("(")].strip()                
                
                funcname_full=""
                
                #Get quotes
                quotes=[]
                index=0
                for token in line:
                    if isinstance(token, fpl_lib.quotetoken):
                        quotes.append(index)
                        
                    index+=1
                     

                #Get parameters
                commas=[]
                index=0
                z=0
                inquote=False
                for token in line:
                    if len(quotes)>z and index == quotes[z]:
                        inquote = not inquote
                        z+=1
                        if z==len(quotes):
                            z-=1
                                                    
                        index+=1
                        continue
                        
       
                    if not inquote:
                        if isinstance(token, fpl_lib.commatoken):
                            commas.append(index)
                            
                    index+=1
                    
                    
                parameters=[]
                for n in range(len(commas)+1):
                    parameters.append([])
                      
                index2=0
                for n in range(len(funcname),len(line)):
                    token=line[n]
    
                    if isinstance(token, fpl_lib.closeparenthesistoken):
                        parameters[index2].append(token)
                        break
                    
                    if isinstance(token, fpl_lib.commatoken):
                        if n in commas:
                            index2+=1
                        
                    parameters[index2].append(token)
                                   

                for n in range(len(parameters)):
                    for i in range(len(parameters[n])):
                        if i==0:
                            continue
                        funcname_full+=parameters[n][i].token
                        
                funcparam=funcname_full[0:len(funcname_full)-1]
                
                
                #Split funcparam on spaces, but not on spaces in quotes
                
                #Get quotes
                quotes=[]
                index=0
                for char in funcparam:
                    if char=="\"":
                        quotes.append(index)
                        
                    index+=1
                
                #Get parameters
                spaces=[]
                index=0
                z=0
                inquote=False
                for char in funcparam:
                    if len(quotes)>z and index == quotes[z]:
                        inquote = not inquote
                        z+=1
                        if z==len(quotes):
                            z-=1
                                                    
                        index+=1
                        continue
                        
       
                    if not inquote:
                        if char==" ":
                            spaces.append(index)
                            
                    index+=1
                  
                funcparam_strbuf=""
                funcparam_buf=[]
                spaceindex=0
                for index in range(len(funcparam)):
                    if index==spaces[spaceindex]:
                        spaceindex+=1
   
                        funcparam_buf.append(funcparam_strbuf)
                        funcparam_strbuf=""
                        
                        if spaceindex==len(spaces):
                            funcparam_buf.append(funcparam[index+1:])
                            break
                        
                        continue
                    funcparam_strbuf+=funcparam[index]
                    
           
                funcparam=funcparam_buf
                ###
                
                #Todo: add parameter auto placement (like regular command)
                command=functions[funcname][2]
                command_order=functions[funcname][3]
                
                for n in range(len(parameters)):
                    parameter=parameters[n]
                        
                    name=""

                    for i in range(len(parameter)):
                        if isinstance(parameter[i], fpl_lib.equaltoken):
                            break
                        
                        if isinstance(parameter[i], fpl_lib.text):
                            name+=parameter[i].token


                    if name in command_order:
                        evalparam_=parameter[i+1:len(parameter)]
                        
                        evalparam=[]
                        for token in evalparam_:
                            evalparam.append(token.token)
                            
                                               
                        
                        if len(evalparam)>0 and evalparam[len(evalparam)-1]==")":
                            evalparam=evalparam[0:len(evalparam)-1]
                            
                        if len(evalparam)>0:
                            evalparam=fpl_env.eval_fpl(evalfpl, "".join(evalparam))
                        else:
                            evalparam=""
                    
                        
                        command[name]=str(evalparam)
                                                
                    else:
                        index=0
                        for token in parameter:
                            if isinstance(token, fpl_lib.text) or isinstance(token, fpl_lib.quotetoken):
                                break
                                
                            index+=1
                        

                        evalparam_=parameter[index:len(parameter)]
  
                        evalparam=[]
                        for token in evalparam_:
                            evalparam.append(token.token)
                            
                        if len(evalparam)>0 and evalparam[len(evalparam)-1]==")":
                            evalparam=evalparam[0:len(evalparam)-1]
                          
                        if len(evalparam)>0:
                            evalparam=fpl_env.eval_fpl(evalfpl, "".join(evalparam))
                        else:
                            evalparam=""
                        
                        command[command_order[n]]=str(evalparam)
                        
                #Actually run function
                evalfpl_func=fpl_env()
                
                for item in command:
                    expr=item+"="+"\""+command[item]+"\""
                    evalfpl_func.exec_fpl(expr)
                    
                fpl_exec_tokenized(functions[funcname][0],functions[funcname][1],commands_origin,evalfpl_func)
                del evalfpl_func
                
    
                
                
            #Variable
            else:    
                fpl_env.exec_fpl(evalfpl, vartokens)
            
            
        else:    
            command_=commands[0] 
            
            #special=[]
            quotes=[]
            
            #Get quotes
            index=0
            for token in line:
                if isinstance(token, fpl_lib.quotetoken):
                    quotes.append(index)
                    
                index+=1
             
            """
            #Get brackets
            index=0
            for token in line:
                if isinstance(token, fpl_lib.openbrackettoken) or isinstance(token, fpl_lib.closebrackettoken):
                    special.append(index)
                    
                index+=1
                
            special=sorted(special)
            """

            #Get parameters
            commas=[]
            index=0
            z=0
            inspecial=False
            for token in line:
                if len(quotes)>z and index == quotes[z]:
                    inspecial = not inspecial
                    z+=1
                    if z==len(quotes):
                        z-=1
                                                
                    index+=1
                    continue
                

   
                if not inspecial:
                    if isinstance(token, fpl_lib.commatoken):
                        commas.append(index)
                        
                index+=1
            
                
            parameters=[]
            for n in range(len(commas)+1):
                parameters.append([])
                


            index2=0
            for n in range(1,len(line)):
                token=line[n]

                if isinstance(token, fpl_lib.closeparenthesistoken):
                    parameters[index2].append(token)
                    break
                
                if isinstance(token, fpl_lib.commatoken):
                    if n in commas:
                        index2+=1
                    
                parameters[index2].append(token)
                

            #for parameter in parameters:
            #    print(parameter, end="\n\n")
                
        

            if command_=="print":
                command={"text":"", "end":"\n"}
                command_order=["text","end"]
                
                for n in range(len(parameters)):
                    parameter=parameters[n]
                        
                    name=""

                    for i in range(len(parameter)):
                        if isinstance(parameter[i], fpl_lib.equaltoken):
                            break
                        
                        if isinstance(parameter[i], fpl_lib.text):
                            name+=parameter[i].token
                        


                    if name in command_order:
                        evalparam_=parameter[i+1:len(parameter)]
                        
                        evalparam=[]
                        for token in evalparam_:
                            evalparam.append(token.token)
                            
                                               
                        
                        if len(evalparam)>0 and evalparam[len(evalparam)-1]==")":
                            evalparam=evalparam[0:len(evalparam)-1]
                            
                        if len(evalparam)>0:
                            evalparam=fpl_env.eval_fpl(evalfpl, "".join(evalparam))
                        else:
                            evalparam=""
                    
                        
                        command[name]=evalparam
                                                
                    else:
                        index=0
                        for token in parameter:
                            if isinstance(token, fpl_lib.text) or isinstance(token, fpl_lib.quotetoken):
                                break
                                
                            index+=1
                        

                        evalparam_=parameter[index:len(parameter)]
  
                        evalparam=[]
                        for token in evalparam_:
                            evalparam.append(token.token)
                            
                        if len(evalparam)>0 and evalparam[len(evalparam)-1]==")":
                            evalparam=evalparam[0:len(evalparam)-1]
                          
                        if len(evalparam)>0:
                            evalparam=fpl_env.eval_fpl(evalfpl, "".join(evalparam))
                        else:
                            evalparam=""
                        
                        command[command_order[n]]=evalparam
                        
                print(command["text"], end = command["end"])
                
            if command_=="if":
                command={"expression":"True"}
                command_order=["expression"]
                
                for n in range(len(parameters)):
                    parameter=parameters[n]
                        
                    name=""
    
                    for i in range(len(parameter)):
                        if isinstance(parameter[i], fpl_lib.equaltoken):
                            break
                        
                        if isinstance(parameter[i], fpl_lib.text):
                            name+=parameter[i].token
    
    
                    if name in command_order:
                        evalparam_=parameter[i+1:len(parameter)]
                        
                        evalparam=[]
                        for token in evalparam_:
                            evalparam.append(token.token)


                        if len(evalparam)>0:
                            pass
                        else:
                            evalparam=""
                    
                        
                        command[name]=evalparam
                                                
                    else:
                        index=0
                        for token in parameter:
                            if isinstance(token, fpl_lib.text) or isinstance(token, fpl_lib.quotetoken):
                                break
                                
                            index+=1
                        
    
                        evalparam_=parameter[index:len(parameter)]
      
                        evalparam=[]
                        for token in evalparam_:
                            evalparam.append(token.token)
                            
                        
                        if len(evalparam)>0:
                            pass
                        else:
                            evalparam=""
                        
                        command[command_order[n]]=evalparam
                        
             
                if not fpl_env.eval_fpl(evalfpl, "".join(command["expression"][0:len(command["expression"])-1])):
                    nexttabs=[i for i,x in enumerate(tabs) if x==tablevel]
                    

                    try:
                        lineindex=nexttabs[nexttabs.index(lineindex)+1]
                        #print(lineindex)
                    
                        lineindex-=1
                        break
                    except IndexError:
                        return
                    
                    
                
            if command_=="while":
                command={"expression":"True"}
                command_order=["expression"]
                
                for n in range(len(parameters)):
                    parameter=parameters[n]
                        
                    name=""
    
                    for i in range(len(parameter)):
                        if isinstance(parameter[i], fpl_lib.equaltoken):
                            break
                        
                        if isinstance(parameter[i], fpl_lib.text):
                            name+=parameter[i].token
    
    
                    if name in command_order:
                        evalparam_=parameter[i+1:len(parameter)]
                        
                        evalparam=[]
                        for token in evalparam_:
                            evalparam.append(token.token)


                        if len(evalparam)>0:
                            pass
                        else:
                            evalparam=""
                    
                        
                        command[name]=evalparam
                                                
                    else:
                        index=0
                        for token in parameter:
                            if isinstance(token, fpl_lib.text) or isinstance(token, fpl_lib.quotetoken):
                                break
                                
                            index+=1
                        
    
                        evalparam_=parameter[index:len(parameter)]
      
                        evalparam=[]
                        for token in evalparam_:
                            evalparam.append(token.token)
                            
                        
                        if len(evalparam)>0:
                            pass
                        else:
                            evalparam=""
                        
                        command[command_order[n]]=evalparam
                  
                    
                if fpl_env.eval_fpl(evalfpl, "".join(command["expression"][0:len(command["expression"])-1])):
                    nexttabs=[i for i,x in enumerate(tabs) if x==tablevel]
                    
                    if nexttabs.index(lineindex)==len(nexttabs)-1:
                        lineindex_last=len(lines)-1
                    
                    else: 
                        lineindex_last=nexttabs[nexttabs.index(lineindex)+1]-1
                    
                    
                    #NOTE TO SELF: LINEINDEX_LAST IS THE INDEX OF LAST COMMAND IN WHILE LOOP
                    
                    inloop["inloop"]=True
                    inloop["looptype"]=command_
                    inloop["lastline"]=lineindex_last
                    inloop["firstline"]=lineindex
                    inloop["wasinloop"]=True
                    
                    
                    
                    """
                    lineindex+=1
                    if lineindex>=len(lines):
                        break
                    
                    continue
                    """
                else:
                    inloop["inloop"]=False
                    inloop["wasinloop"]=True
                    
                    
                    
            if command_=="function":
                funcname_full=""
                
                for n in range(len(parameters)):
                    for i in range(len(parameters[n])):
                        if i==0:
                            continue
                        funcname_full+=parameters[n][i].token
                        

                #Get parenthesis
                parenthesis_=[]
                
                index=0
                for token in funcname_full:
                    if token=="(" or token==")":
                        parenthesis_.append(index)
                
                    index+=1
                    
                funcname=funcname_full[0:parenthesis_[0]]
                funcparam=funcname_full[parenthesis_[0]+1:parenthesis_[len(parenthesis_)-1]]
                
                #Split funcparam on spaces, but not on spaces in quotes
                
                #Get quotes
                quotes=[]
                index=0
                for char in funcparam:
                    if char=="\"":
                        quotes.append(index)
                        
                    index+=1
                
                #Get parameters
                spaces=[]
                index=0
                z=0
                inquote=False
                for char in funcparam:
                    if len(quotes)>z and index == quotes[z]:
                        inquote = not inquote
                        z+=1
                        if z==len(quotes):
                            z-=1
                                                    
                        index+=1
                        continue
                        
       
                    if not inquote:
                        if char==" ":
                            spaces.append(index)
                            
                    index+=1
                  
                funcparam_strbuf=""
                funcparam_buf=[]
                spaceindex=0
                for index in range(len(funcparam)):
                    if index==spaces[spaceindex]:
                        spaceindex+=1
   
                        funcparam_buf.append(funcparam_strbuf)
                        funcparam_strbuf=""
                        
                        if spaceindex==len(spaces):
                            funcparam_buf.append(funcparam[index+1:])
                            break
                        
                        continue
                    funcparam_strbuf+=funcparam[index]
                    
           
                funcparam=funcparam_buf
                ###
                
                
                nexttabs=[i for i,x in enumerate(tabs) if x==tablevel]
                    
                if nexttabs.index(lineindex)==len(nexttabs)-1:
                    lineindex_last=len(lines)-1
                
                else: 
                    lineindex_last=nexttabs[nexttabs.index(lineindex)+1]-1
                    
                funccode_=lines[lineindex+1:lineindex_last+1]
                functabs=tabs[lineindex+1:lineindex_last+1]
            
                for n in range(len(functabs)):
                    functabs[n]-=tabs[lineindex+1]
                
                funccode_buf=[]
                funccode=[]
                
                for n in range(len(funccode_)):
                    line_func=funccode_[n]
                    line_func.append(fpl_lib.newlinetoken("\n"))
                    funccode_buf.append(line_func)
                    
                for line_buffunc in funccode_buf:
                    for token in line_buffunc:
                        funccode.append(token)
                    
                
                lineindex=lineindex_last
                
                command={}
                command_order=[]
                
                for item in funcparam:
                    if len(item)==0:
                        continue
                    
                    if "=" not in item:
                        command_order.append(item)
                        command[item]=""
                    if "=" in item:
                        command_order.append(item[0:item.find("=")])
                        command[item[0:item.find("=")]]=item[item.find("=")+1:]
                
                if funcname==command_:
                    raise SyntaxError("Function name cannot be 'function'")
                
            
                
                functions[funcname]=[funccode,functabs,command,command_order]
                
                """
                #Actually run function
                evalfpl_func=fpl_env()
                
                for item in funcparam:
                    evalfpl_func.exec_fpl(item)
                    
                fpl_exec_tokenized(functions[funcname][0],functions[funcname][1],commands_origin,evalfpl_func)
                del evalfpl_func
                """
                
                
                
                        
         
        if inloop["inloop"]==True and lineindex==inloop["lastline"]:
            if inloop["looptype"]=="while":
                lineindex=inloop["firstline"]
    
                continue
            
        if inloop["inloop"]==False and inloop["wasinloop"]==True:
            nexttabs=[i for i,x in enumerate(tabs) if x==tablevel]

            try:
                lineindex=nexttabs[nexttabs.index(lineindex)+1]#+1
            except IndexError:
                return
                        
            inloop["wasinloop"]=False
            continue
    

        lineindex+=1
        
        if lineindex>=len(lines):
            break


def fpl_exec_raw(program, commands):
    tokenizer=fpl_lib.tokenizer(program, commands) 
    fpl_lib.tokenizer.tokenize(tokenizer)
    tokens=tokenizer.tokens
    tabs=tokenizer.tabs
    
    #print(tokens)
    
    
    
    
    #Print info

                       
    """
    for n in range(len(tabs)):
        print(tabs[n])
        linex_=lines[n]
        for token in linex_:
            print(token.token, end="")
        print()
        print()
    

    #Print out tokens
    for token in tokens: 
        if isinstance(token, fpl_lib.constant):
            print("Object is a constant:  ", end='')
        if isinstance(token, fpl_lib.token):
            print("Object is a token:  ", end='')
            
        print(type(token), end = '')
        
        print("  token is: '"+token.token+"'")
    
    print()
    
    print(str(len(tokens))+" tokens.\n\n"+"-"*80+"\n")
        
    """
    
    #Create enviornment
    evalfpl=fpl_env()
    
    fpl_exec_tokenized(tokens,tabs,commands,evalfpl)
    
    
            
        

        
        
    
    

    

commands=["print","if","while","function"]
        

if __name__=="__main__":
    loader=fpl_loader.loader("program.txt")
    program=fpl_loader.loader.load(loader)  

    fpl_exec_raw(program, commands)

    
    
