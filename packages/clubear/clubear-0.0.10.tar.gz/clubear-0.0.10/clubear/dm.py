import pandas as pd
import glob,os,time,IPython
import numpy as np

'''
This module is develped for a quick management for multiple datafiles.
We assume that a number of big data files are contained in one common
directory. Then, we wish to answer the following important questions:
    
(1) How many CSV files do we have in the target directory? what about 
their sizes in G and lines? How about their shapes?

(2) Do they have headers? If so, are their headers consistent with each
other or note? Do they have an nonempty intersection.

According to the the answers of the above questions, we propose the following
two methods to combine all the files into one single BIGDATA file for 
next stage analysis. 

(1) The 1st method is write(), it is useful if all the data files have 
appropriately defined headers. Accordingly, write() merges all the CSV files 
into one BIGDATA file. Only those columns exists in all CSV files are included.
Those columns are not included by **every** csv file is dropped.

(2) The 2nd method is dump(), it is useful if all the data files have no 
headers. However, the contains the exactly the same number of columns.
Then, dump() simply merge all the files into one single BIGDATA file.
'''

class manager(object):
    
    def demo():
        
        greeting='''
To demonstrate the data manager method, we need to creat a folder
named 'demodata' in your current directory. In the directory, we 
will simulate 10 CSV datasets, named: CluBearDemoData.X.csv. For 
each CSV file there contains a number of variables and the 'sales' 
one can be treated for response for regression.

**WARNING**: 'demodata' is a folder created for clubear demo only. As
a result, please do *NOT* place any personal file in this 'demodadta' 
folder for they are to be *DELETED* completely. Once your files are 
deleted, they can NEVER be recovered! By answering 'YES', any files
in the demodata folder (if exists) will be completely removed.
'''
        print(greeting);print('')
        userinput=input('Do you want to proceed [YES/No]:')
        if userinput != 'YES': return('manager.demo: demo data cannot be generated without user permission.')
        
        print('')
        if not os.path.exists('demodata'): os.makedirs('demodata')
        files=os.listdir('demodata')
        [os.remove('demodata/'+each) for each in files]

        nfiles=9;ss=10000;
        heads=['gender','age','height','weight','region','company','brand','price','sales']
        ncov=len(heads)
        headline=','.join(heads)+'\n'
        for j in range(nfiles):
            filename='CluBearDemoData.'+str(j)+'.csv'
            f=open('demodata/'+filename,'w')
            f.write(headline)
            for i in range(ss):
                gender='M'; 
                if np.random.normal(0,1,1)>0: gender='F'
                age=int(np.round(20+50*np.random.uniform()))
                height=np.round(1.5+0.5*np.random.uniform(),2)
                weight=int(100+100*np.random.uniform())
                region=chr(int(65+25*np.random.uniform()))
                company=chr(int(70+5*np.random.uniform()))+chr(int(65+5*np.random.uniform()))
                brand=chr(int(75+10*np.random.uniform()))+chr(int(80+10*np.random.uniform()))
                price=np.round(np.random.uniform()*100)
                sales=np.random.normal(0,1,1)+0.5*np.sqrt(age)+0.3*(gender=='F')
                sales=sales-0.2*np.log(price)+0.2*(region=='Z')-0.35*(region=='A')
                sales=np.round(np.exp(sales))[0]
                line=[gender,age,height,weight,region,company,brand,price,sales]
                line=[str(each) for each in line]
                line=','.join(line)+'\n'
                f.write(line)
            f.close()
            print('Demo datasets generated [',j+1,'/',nfiles,'] :',filename)
        

        demostr='''
import clubear as cb
dm=cb.manager("demodata/") #initiate a dm object. 
dm.files #the file names without path.
dm.sizes #the file sizes in bytes.
dm.nr #the number of rows in each file.
dm.nc #the number of columns in each file.
dm.heads #the columns contained in each file.
dm.Heads #the columns contained in EVERY file.
dm.write() #do a test run for write
dm.write("clubear.csv") #do a full run with headers
'''
        print(demostr)
    
    
    def __init__(self,path):
        
        if not os.path.exists(path): print('manager: The directory dose not exists!'); return
        if not os.path.isdir(path): print('manager: This is not a director at all!'); return
        
        '''List all the CSV files under the director'''
        csvfiles = glob.glob(path+"*csv")
        csvfiles = sorted(csvfiles)
        isfiles=list(map(os.path.isfile,csvfiles))
        csvfiles = [csvfiles[each] for each in range(len(csvfiles)) if isfiles[each] == True] 
        if len(csvfiles)==0: print('manager: No CSV file found in the director!'); return
        
        '''short file names without path information'''
        shortfiles=[each[len(path):] for each in csvfiles]

        
        '''Count the number of lines in each file'''
        IPython.display.clear_output(wait=True)
        print('Total',len(csvfiles),'files found in path=',path)
        print('')
        nr = np.array([0 for each in csvfiles])
        for kk in range(len(csvfiles)):
            nr[kk]=sum(1 for line in open(csvfiles[kk],encoding='iso8859-1'))
            nr[kk]=nr[kk]-1 #eliminate the header line
            print(csvfiles[kk],nr[kk],'(',kk+1,'/',len(csvfiles),')')
        mlines=np.round(nr/10**3,2)

        '''Open each CSV file and get its first row and assume they are headers'''
        openfiles=[open(each,encoding='iso8859-1') for each in csvfiles]
        heads = [each.readline().replace("\n","").replace('\"','').replace("\'","").split(',') for each in openfiles]
        
        '''The number of columns in each CSV file'''
        nc = [len(each) for each in heads]
        
        '''Output at most 3 column headers for inspection. The number of characters'''
        '''contained in each header is constrainted to be no more than maxstrlen.'''
        maxstrlen=10
        maxm=np.min([np.min(nc),3])
        topheads=[each[0:maxm] for each in heads]
        for i in range(len(topheads)):
            for j in range(maxm):
                topheads[i][j]=topheads[i][j][:maxstrlen]
                
        '''Heads contains those columns commonly shared by EVERY file'''
        '''the order fo Heads is determined by its order in the 1st CSV file'''
        Heads = sorted(list(set.intersection(*map(set,heads))))
        Heads = [each for each in heads[0] if each in Heads]
        
        '''each file sizes in G bytes'''
        filesizes=np.round(np.array(list(map(os.path.getsize,csvfiles)))/(2.0**20),3)
        
        '''output to screen for user inspection'''
        output=pd.DataFrame(list(zip(shortfiles,filesizes,mlines,nc,topheads)))
        output.columns=['files','sizes','nr','nc','heads']
        IPython.display.clear_output(wait=True)
        print('Total',len(csvfiles),'files found with ',len(Heads),'common columns and ',np.sum(nr),'lines.')
        print('')
        print(output)
        print('')
        print('* files: a list of csvfile names without path information; sizes: the sizes of the files in M bytes')
        print('* nr: the number of rows contained in the file in 10**3; nc: the number of columns contained in the file')
        print('');
        print('The following',len(Heads),'Heads are found in EVERY file and can be used for output:')
        print('\n',Heads)
        print('')
        
        '''global variables shared by the class'''
        self.csvfiles = csvfiles
        self.totlines=np.sum(nr)        
        self.path = path
        
        self.nc = np.array(nc)
        self.nr = np.array(nr)
        self.heads = heads
        self.files = shortfiles
        self.sizes = list(map(os.path.getsize,csvfiles))
        self.Heads = Heads
    
    '''The write() method is used to merge CSV files **with** headers'''
    def write(self,pathfile='_CluBearTest_.csv'):
        
        if len(self.Heads)==0: print('manager: No common column can be writen out!'); return
        
        '''Always remove the target file so that a new file can be created'''
        if os.path.exists(pathfile): os.remove(pathfile)
        
        '''If no filename given by user then do a test run write() get from each file '''
        '''its 1st observation (not header) line and then output them to a target file.'''
        if pathfile=='_CluBearTest_.csv':
            is_first_file = True       
            for each in self.csvfiles:
                reader=pd.read_csv(each,iterator=True,encoding='iso8859-1')
                chunk=reader.get_chunk(1)[self.Heads]
                chunk.to_csv(pathfile,mode='a',index=0,header=is_first_file)
                is_first_file=False

        '''If filename is given by user then do a test run write() get from each file '''
        '''its all observation lines and then output them to a target file.'''
        if pathfile!='_CluBearTest_.csv':
            
            '''This is the file for output'''
            f=open(pathfile,'w',encoding='iso8859-1')
            
            '''output the header line'''
            f.write(','.join(self.Heads)+'\n')
            
            '''oklines counts how many lines have been ouputed'''
            oklines=0
            
            '''output each CSV file'''
            for each in self.csvfiles:
                reader=open(each,encoding='iso8859-1')
                
                '''read in the line and this is the headerline'''
                firstline=next(reader).replace('\n','').replace('\"','').replace("\'","").split(',')
                
                '''find the column positions of those variables in Heads'''
                pos=[firstline.index(each) for each in self.Heads]
                
                '''remember oklines should add one'''
                oklines=oklines+1
                
                '''start to read and write data lines'''
                for line in reader:
                    
                    '''read in data line and keep those columns in Heads'''
                    newline=line.replace('\n','').replace('\"','').replace("\'","").split(',')
                    data=[newline[each] for each in pos]
                    
                    '''output to the target file'''
                    data=','.join(data)+'\n'
                    f.write(data)
                    oklines=oklines+1
                    
                    '''for every 10**5 lines the progress % is updated'''
                    if (oklines%10**5==0)|(oklines==self.totlines):
                        progress='%.2f'%(100*oklines/self.totlines)
                        IPython.display.clear_output(wait=True)
                        print("Mission accomplished: ", progress,'% for a total of ',self.totlines,'lines.' )                    
            f.close()
            
        '''data target data is created. we sould read its top 10 lines and '''
        '''output them to the screen for user inspection'''
        df=pd.read_csv(pathfile,iterator=True,encoding='iso8859-1')
        df=df.get_chunk(10)
        if os.path.exists('_CluBearTest_.csv'): os.remove(pathfile)
        return df

    
    '''The dump() method is used to merge CSV files **without** headers'''
    def dump(self,pathfile='_CluBearTest_.csv'):
        
        '''Always remove the target file so that a new file can be created'''
        if os.path.exists(pathfile): os.remove(pathfile)
        
        '''This is the target file for output'''
        f=open(pathfile,'w',encoding='iso8859-1')
        
        '''Since those files have no headers, we are going to create headers for'''
        '''them. How many headers are needed? This is determined by the maximum '''
        '''number of columns contained in each CSV file.'''
        max_num_columns=np.max(self.nc)
        column_names=",".join(["V"+str(i) for i in range(max_num_columns)])+'\n'
        f.write(column_names)
        
        '''If no user input is given then do a test run'''
        if pathfile=='_CluBearTest_.csv': [f.write(next(open(each,encoding='iso8859-1'))) for each in self.csvfiles]
            
        '''If user input is given, we then do a full size run'''
        if pathfile!='_CluBearTest_.csv':
            
            '''start to record how many lines outputed'''
            oklines=0
            
            '''do for each CSV file'''
            for each in self.csvfiles:
                
                '''do for each line'''
                for line in open(each,encoding='iso8859-1'):
                    
                    '''write to the target file'''
                    f.write(line)
                    
                    '''update how many lines outputed'''
                    oklines=oklines+1
                    
                    '''update the progress % for every 10**5 lines'''
                    if (oklines%10**5==0)|(oklines==self.totlines):
                        progress='%.2f'%(100*oklines/self.totlines)
                        IPython.display.clear_output(wait=True)
                        print("Mission accomplished: ", progress,'% for a total of ',self.totlines,'lines.' )                    
        f.close()

        '''data target data is created. we sould read its top 10 lines and '''
        '''output them to the screen for user inspection'''
        df=pd.read_csv(pathfile,iterator=True,encoding='iso8859-1')
        df=df.get_chunk(10)
        if os.path.exists('_CluBearTest_.csv'): os.remove(pathfile)
        return df