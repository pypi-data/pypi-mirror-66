from .sub import subsample   
from .fun import ispump
import IPython
import pandas as pd
import numpy as np
import os


class pump:

    def demo():
        demostr = '''
import clubear as cb
pathfile='/clubear/data/single_files/airline.csv'
pp=cb.pump(pathfile) #start a new data pump
pp.drop=['TaxiOut','Dest'] #drop some data
pp.niter=5        #run pump how many times
pp.run()          #run pump to get dataframe
'''
        print(demostr)

    def __init__(self, pathfile):
        
        '''Check whether the file exists or correct.'''
        if not os.path.exists(pathfile): print('pump: This file dose not exists!'); return
        if not os.path.isfile(pathfile): print('pump: This is not a file!'); return;
        self.pathfile = pathfile
        self.db = subsample(pathfile)

        '''Determine subsize automatically'''
        tmpfile = open(pathfile, encoding='iso8859-1')
        tmpfile.seek(0, 2)
        total_file_size = tmpfile.tell()
        tmpfile.seek(0, 0)
        line_counter = 0
        number_of_lines = 100
        while line_counter < number_of_lines:
            line = tmpfile.readline()
            line_counter = line_counter+1
        linesize = tmpfile.tell()/number_of_lines
        self.popsize = np.round(total_file_size/linesize).astype('int32')
        self.subsize = np.ceil(np.sqrt(self.popsize)).astype('int32')

        '''Determine data type automatically'''
        df = self.db.rand_sample(10000)
        self.heads = list(df.columns)
        ncolumns = len(self.heads)
        for each in self.heads:
            df[each] = pd.to_numeric(df[each], errors='coerce')
        missing_prob = np.mean(np.isnan(np.array(df)), axis=0)
        self.qnames = [self.heads[each]
                       for each in range(ncolumns) if missing_prob[each] < 0.1]
        self.cnames = [each for each in self.heads if each not in self.qnames]
        self.drop = []

        df = self.db.rand_sample(1)
        for each in self.qnames:
            df[each] = pd.to_numeric(df[each], errors='coerce')

    def run(self):
        '''check we have some columns left for output'''
        self.qnames=[each for each in self.qnames if each in self.heads]
        self.cnames=[each for each in self.cnames if each in self.heads]
        vlist = list(set(self.qnames+self.cnames))
        vlist = [each for each in vlist if each not in self.drop]
        self.drop=[each for each in self.heads if each not in vlist]
        if len(vlist)==0: return('pump.run: No columns can be outputed!')
        
        '''make sure that subsize cannot be smaller than 1'''
        self.subsize=int(np.max([self.subsize,1]))
        
        df = self.db.rand_sample(self.subsize); df = df[vlist]
        for each in self.qnames: df[each] = pd.to_numeric(df[each], errors='coerce')
        if len(self.qnames) > 0:
            data = np.array(df[self.qnames]).astype('float')
            mu = np.mean(data, axis=1)
            flag = (np.abs(mu) >= 0) & (np.abs(mu) < 1.0e+15)
            df = df.iloc[flag == True]
        return df


class check(object):

    def demo():
        demostr = '''
import clubear as cb
pathfile='/clubear/data/single_files/airline.csv'
pp=cb.pump(pathfile) #start a new data pump
ck=cb.check(pp)      #create a pump checker
ck.stats() #check all quantitative varialbes
ck.table() #check all qualitative variables

ck.qnames=['Distance','ArrDelay']
ck.stats() #check the focused quant. variables

ck.cnames=['Year','Month','SecurityDelay']
ck.table() #check the focused quali. variables
ck.table(True)    #view the detailed table
'''
        print(demostr)

    def __init__(self, pp):
        self.pp = pp
        
        '''check whether the input is a pump first'''
        pump_check=ispump(self.pp)
        if pump_check != 'YES': print(pump_check); return
        
        '''initialization'''
        df = self.pp.run()
        self.heads = list(df.columns)
        self.ncolumns=len(self.heads)
        self.qnames = [each for each in self.heads if str(df.dtypes[each]) != 'object']
        self.cnames = [each for each in self.heads if str(df.dtypes[each]) == 'object']

    def stats(self, niter=10,names=[]):
        '''run at least one iteration'''
        niter=int(np.max([1,niter]))
        
        '''check whether the input is a pump first'''
        pump_check=ispump(self.pp)
        if pump_check != 'YES': print(pump_check); return
     
        '''check whether we have something to stats'''
        df = self.pp.run()
        self.heads = list(df.columns)
        if not isinstance(names,list): return('check.stats: The names input must be a list!')
        if len(names)>0: self.qnames=names
        self.qnames=[each for each in self.qnames if each in self.heads]
        if len(self.qnames)==0: return('check.stats: No quantitative variable can be checked!')
        
        '''main part for computing statistics'''
        ncov = len(self.qnames)
        N = np.zeros(niter)
        MU = np.zeros([niter, ncov])
        Min = np.zeros([niter, ncov])
        Med = np.zeros([niter, ncov])
        Max = np.zeros([niter, ncov])
        SD = np.zeros([niter, ncov])
        Skew = np.zeros([niter, ncov])
        Kurt = np.zeros([niter, ncov])
        
        for i in range(niter):
            '''get data and make it float'''
            df = self.pp.run()
            df = np.array(df[self.qnames]).astype('float')
            
            '''The 1st bach of stat *without* central'''
            N[i] = df.shape[0]
            MU[i] = np.mean(df, axis=0)
            Min[i] = np.min(df, axis=0)
            Med[i] = np.median(df, axis=0)
            Max[i] = np.max(df, axis=0)

            '''The 2nd batch of stat *with* central'''
            df = df-MU[i]
            SD[i] = np.mean(df**2, axis=0)
            Skew[i] = np.mean(df**3, axis=0)
            Kurt[i] = np.mean(df**4, axis=0)

            '''organize for interactive output'''
            MyN = np.mean(N[:(i+1)])
            MyMU = np.mean(MU[:(i+1)], axis=0)
            MyMin = np.min(Min[:(i+1)], axis=0)
            MyMed = np.median(Med[:(i+1)], axis=0)
            MyMax = np.max(Max[:(i+1)], axis=0)
            MySD = np.sqrt(np.mean(SD[:(i+1)], axis=0))+1.0e-12
            MySkew = np.mean(Skew[:(i+1)], axis=0)/MySD**3
            MyKurt = np.mean(Kurt[:(i+1)], axis=0)/MySD**4
            output = pd.DataFrame(list(zip(MyMU, MySD, MyMin, MyMed, MyMax, MySkew, MyKurt)))
            output.columns = ['Mean', 'SD', 'Min','Med', 'Max', 'Skew', 'Kurt']
            output.index = self.qnames
            
            '''output to screen for interactive analysis'''
            IPython.display.clear_output(wait=True)
            pd.set_option('display.float_format', lambda x: '%.3f' % x)
            progress = np.round((i+1)/niter*100, 2)
            print('Task accomplished: ', progress,
                  '% for a total of ', niter, 'random replications.')
            print('The averaged subsample sizes are:', np.round(MyN, 1), '.')
            print('')
            print(np.round(output, 3))

    def table(self, tv=False,niter=10,names=[]):
        '''run at least one iteration'''
        niter=int(np.max([1,niter]))
        
        '''check whether the input is a pump first'''
        pump_check=ispump(self.pp)
        if pump_check != 'YES': print(pump_check); return

        '''check whether we have something for table'''
        df = self.pp.run(); self.heads = list(df.columns)
        if not isinstance(names,list): return('check.table: The names input must be a list!')
        if len(names)>0: self.cnames=names
        self.cnames=[each for each in self.cnames if each in self.heads]
        if len(self.cnames) == 0: return('check.table: No categorical variable can be used for table.')
        ncov = len(self.cnames)

        '''a lists of sets for level values'''
        value_sets = [set() for each in range(ncov)]
        
        '''a list of Series for elvel counts'''
        tables = [pd.Series() for each in range(ncov)]
        
        for n in range(niter):
            df = self.pp.run()[self.cnames]
            for j in range(ncov):
                '''current subsample data computing'''
                new = list(df[self.cnames[j]].astype('str'))
                value_sets[j] = value_sets[j] | set(new)
                value_list = sorted(list(value_sets[j]))
                value_counts = [new.count(each) for each in value_list]
                
                '''for current count results into Series'''
                pds = pd.Series(value_counts)
                pds.index = value_list
                
                '''merge the current result with the history'''
                current_index = tables[j].index
                pds[current_index] = pds[current_index]+tables[j][current_index]
                tables[j] = pds

            '''for interactive outputs'''
            IPython.display.clear_output(wait=True)
            pd.set_option('display.float_format', lambda x: '%.1f' % x)
            total_counts = int(np.mean([sum(tables[each])
                                        for each in range(ncov)]))
            print("Mission Completed: ", np.round(100.0*(n+1)/niter, 2), '% for a total of',
                  niter, 'iterations for totally', total_counts, 'counts.')
            print("  ")
            for j in range(ncov):
                args = np.argsort(-tables[j])
                tables[j] = tables[j][args]
                clevels = list(tables[j].index)
                cvalues = list(tables[j])
                print('[', j, '] Total', len(clevels),
                      'levels detected for the variable *', self.cnames[j], '*')
                if tv == True:
                    prob = cvalues/np.sum(cvalues)*100
                    max_output_number = np.min([len(clevels), 100])
                    for k in range(max_output_number):
                        print(clevels[k], '=', np.round(
                            prob[k], 2), '%', end='|')
                    if len(clevels) > 100:
                        print('* Note: only top 100 levels displayed...')
                    print('')
                    print('')
        self.tables = tables
