import time

author="CluBear Reserch Group" 
version=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

from .dm import manager
from .pp import pump
from .ck import check
from .plt import plot

from .fun import demo
from .fun import ady
from .fun import ispump
