import pandas as pd
import numpy as np

def demo():
    mylist=['subsample','manager','shuffle','pump','check','subreg','dummy']
    mylist=sorted(mylist)
    print('The following',len(mylist),'methods are contained in this package:')
    print('\n',mylist)
    
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
        df=pp.run()
    except:
        return("ispump: The input pump is NOT a pump and has no RUN!")
    if not isinstance(df, pd.DataFrame): return('ispump: The pump RUN output is not a DataFrame!')
    
    return out


