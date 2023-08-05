from .fun import ispump
from .fun import ady

from scipy.stats import norm
import pandas as pd
import numpy as np


import IPython


class subreg:

    def demo():
        demostr = '''
import clubear as cb
filepath='/clubear/data/single_files/airline.csv'
pp=cb.pump(filepath) #start a data pump
reg=cb.subreg(pp,y='ArrTime') #start a reg analyzer
reg.fit()                  #do full model anaysis
reg.x=list(reg.out[reg.out['p.Value']<5].index)
reg.fit(niter=100)  #re-fit on selected variables
'''
        print(demostr)

    def __init__(self, pp, y=""):
        self.pp = pp;self.y=y
        
        '''check whether the input is a pump first'''
        pump_check=ispump(self.pp)
        if pump_check != 'YES': print(pump_check); return
        
        '''if pass the pump test'''
        df = self.pp.run()
        self.heads = list(df.columns)
        self.ncolumns = len(self.heads)
        self.x = [each for each in self.heads if str(df.dtypes[each]) != 'object']
        
        '''check whether there is a good y'''
        if not isinstance(y,str): print('subreg: The response y must be a str!');return
        if not y in self.heads: print('subreg: The response y not found in dataframe!');return
        if df.dtypes[y]=='object': print('subreg: The response y should be numeric!'); return
        self.y=y
        
        '''if passed the pump and y test'''
        self.x=[each for each in self.x if self.x != self.y]
        
        '''number of covariates with intercept'''
        self.ncov = len(self.x)+1;
        
    def fit(self, niter=10):
        '''run at least one iteration'''
        niter=int(np.max([1,niter]))
        
        '''check whether the input is a pump first'''
        pump_check=ispump(self.pp)
        if pump_check != 'YES': print(pump_check); return
        
        '''update heads and ncolumns'''
        df = self.pp.run()
        self.heads = list(df.columns)
        self.ncolumns = len(self.heads)
        
        '''check whether there is a good y'''
        if not isinstance(self.y,str): print('subreg.fit: The response y must be a str!');return
        if not self.y in self.heads: print('subreg.fit: The response y not found in dataframe!');return
        if df.dtypes[self.y]=='object': print('subreg.fit: The response y should be numeric!'); return
        
        '''update the x variables'''
        if not isinstance(self.x,list): return('subreg.fit: The x variable should be a list!'); return
        self.x = [each for each in self.x if each in self.heads]
        self.x = [each for each in self.x if str(df.dtypes[each]) != 'object']
        self.x = [each for each in self.x if each != self.y]        
        
        '''number of covariates with intercept'''
        self.ncov = len(self.x)+1;
        
        
        '''the following is the main computation'''
        BETA = np.zeros([niter, self.ncov])
        SE = np.zeros([niter, self.ncov])
        R2 = np.zeros(niter)
        FSTAT = 0
        
        for i in range(niter):
            df = self.pp.run()
            Y = np.array(df[self.y]).astype('float')
            ss = len(Y)
            df = df.drop(self.y, axis=1)
            df = df[self.x]
            X = np.array(df).astype('float')
            X = np.hstack([np.ones([ss, 1]), X])
            XX = np.matmul(X.T, X)/ss+np.eye(self.ncov)*1.0e-6
            XY = np.matmul(X.T, Y)/ss
            Sigma = np.linalg.inv(XX)
            beta = np.matmul(Sigma, XY)
            yhat = np.matmul(X, beta)
            resid = Y-yhat
            stde = np.sqrt(np.mean(resid**2))
            r2 = 100*(1-stde**2/np.mean((Y-np.mean(Y))**2))
            se = stde*np.sqrt(np.diag(Sigma))/np.sqrt(ss)
            tstat = beta/se
            pvalue = 2*(1-norm.cdf(np.abs(tstat)))

            BETA[i, :] = beta
            SE[i, :] = se
            R2[i] = r2
            MyBeta = np.mean(BETA[:(i+1)], axis=0)
            MySE = np.mean(SE[:(i+1)], axis=0)/np.sqrt(i+1)
            MyZ = MyBeta/(MySE+1.0e-12)
            MyProb = 2*(1-norm.cdf(np.abs(MyZ)))
            MyR2 = np.mean(R2[:(i+1)])

            fstat = np.sum((Y-np.mean(Y))**2)-np.mean(resid**2)
            fstat = fstat/np.mean(resid**2)
            FSTAT = FSTAT+fstat
            DF = (i+1)*(self.ncov-1)
            FZSTAT = (FSTAT/DF-1)*np.sqrt(ss/2)
            FPROB = 10000*(1-norm.cdf(FZSTAT))

            out = pd.DataFrame(list(zip(MyBeta, 100*MySE, MyZ, 100*MyProb)))
            out.columns = ['Estimate', 'Stand.Err', 'Test.Stat', 'p.Value']
            out.index = ['Intercept']+self.x
            IPython.display.clear_output(wait=True)
            pd.set_option('display.float_format', lambda x: '%.3f' % x)
            progress = np.round((i+1)/niter*100, 2)
            print('Task accomplished: ', progress, '% for a total of ',
                  niter, 'random replications.')
            print('The R.Squared = ', np.round(MyR2, 2),
                  '% with global p.value = ', FPROB, '%%.')
            print('')
            print(out)
            print('')
            print(
                '* Estimate: the ordinary least squares estimate; Stand.Err: the standard error;')
            print(
                '* Test.Stat = Estimate / Stand.Err in %; p.Value = the significance level in %.')

            self.out = out
