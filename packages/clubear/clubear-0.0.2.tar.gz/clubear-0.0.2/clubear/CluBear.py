"""Lowercase letters should be used in module names.

    name styles:
    
    module_name,  模块
    package_name,  包
    ClassName,  类
    method_name,  方法
    ExceptionName,   异常
    function_name,  函数
    GLOBAL_VAR_NAME, 全局变量
    instance_var_name,  实例
    function_parameter_name,   参数
    local_var_name.  本变量

"""


from . import subsample as subs
from . import shuffle as sf
from . import manager as dm
from . import pump as pp
from . import subreg as reg

def demo():
    mylist=['subsample','manager','shuffle','pump','check','subreg','dummy']
    mylist=sorted(mylist)
    print('The following',len(mylist),'methods are contained in this package:')
    print('\n',mylist, "\n")


class subsample(subs.subsample):
	pass

class manager(dm.manager):
	pass

class shuffle(sf.shuffle):
	pass   

class pump(pp.pump):
	pass   
    
class check(pp.check):
	pass   
    
class subreg(reg.subreg):
	print("call subreg from CluBear")   
    
def dummy(df,varname,levels):
    ncov=len(levels)
    strlevels=[str(each) for each in levels]
    newname=[varname+'.'+str(each) for each in levels]
    for j in range(ncov): df[newname[j]]=1*(df[varname]==strlevels[j])
