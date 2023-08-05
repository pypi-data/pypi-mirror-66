
def demo():
    mylist=['subsample','manager','shuffle','pump','check','subreg','dummy']
    mylist=sorted(mylist)
    print('The following',len(mylist),'methods are contained in this package:')
    print('\n',mylist)

    
def dummy(df,varname,levels):
    ncov=len(levels)
    strlevels=[str(each) for each in levels]
    newname=[varname+'.'+str(each) for each in levels]
    for j in range(ncov): df[newname[j]]=1*(df[varname]==strlevels[j])
        
def ispump(pp):
    out='YES'
    try:
        df=pp.run()
    except:
        return("CluBear Error: The input pump is NOT a pump and has no RUN!")
    if not isinstance(df, pd.DataFrame): return('CluBear Error: The pump RUN output is not a DataFrame!')
    
    return out


