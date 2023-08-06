import pandas as pd
import numpy as np
import os
    
def ady(df,varname,levels):
    ncov=len(levels)
    strlevels=[str(each) for each in levels]
    strvalues=[str(each) for each in df[varname]]
    newname=[varname+'.'+str(each) for each in levels]
    for j in range(ncov): 
        dummys=[1.0*(each==strlevels[j]) for each in strvalues]
        df[newname[j]]=dummys
    return df
        
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
datasets. The package is developed by CluBear Research Group. You are welcome 
to visit our official website at www.xiong99.com.cn. You are also welcome to 
follow us at our official WeChat account (ID: CluBear). Enjoy!
'''
    print(greeting)
    print('\n',mylist,'\n')
    
    return

