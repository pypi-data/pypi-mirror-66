import pandas as pd
import numpy as np
import os

'''check numeric for a dataframe column'''
def Tom(df,head):
    if not isinstance(df,pd.DataFrame): print('Tom: df should be a dataframe.'); return
    if head not in df.columns: print('Tom: head not found in df.'); return
    df[head]=list(map(TomCheck,df[head]))    

'''check an  object for numeric'''
def TomCheck(x):
    extreme_value=1.0e+15
    x=str(x)
    if len(x)==0: return(extreme_value)
    okset={'+','-','.','0','1','2','3','4','5','6','7','8','9'}
    first_letter=x[0]
    if first_letter not in okset: return(extreme_value)
    if x.count('.')>1: return(extreme_value)
    bad_letters=len(set(x)-okset)
    if bad_letters>0: return(extreme_value)
    return(float(x))

'''add dumy variable'''
def ady(df,varname,levels):
    ncov=len(levels)
    strlevels=[str(each) for each in levels]
    strvalues=[str(each) for each in df[varname]]
    newname=[varname+'.'+str(each) for each in levels]
    for j in range(ncov): 
        dummys=[1.0*(each==strlevels[j]) for each in strvalues]
        df[newname[j]]=dummys
  
'''check whether this is a pump'''
def ispump(pp):
    out='YES'
    try:
        df=pp.go()
    except:
        return("ispump: The input pump is NOT a pump and has no GO!")
    if not isinstance(df, pd.DataFrame): return('ispump: The pump RUN output is not a DataFrame!')
    
    return out

def demo():
    
    mylist=['manager','pump','check']
    mylist=sorted(mylist)
    
    greeting='''
Welcome to CluBear!

This is a package designed for *Interactive* statistical analysis for massive 
datasets. The key idea used here is subsampling. The package is developed by 
CluBear Research Group. You are welcome to visit our official website at 
www.xiong99.com.cn. You are also welcome to follow us at our official WeChat 
account (ID: CluBear). Enjoy!
'''
    print(greeting)
    print('\n',mylist,'\n')
    
    return

