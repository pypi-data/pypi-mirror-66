#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import pandas as pd 
import random
import os
import sys
import time
from multiprocessing import Process, Manager
import multiprocessing
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')

class subsample(object):
    """
    该对象实现对 csv 数据文件的随机排序
    """

    def seed(self, seed):
        """
        设置随机数种子
        """
        random.seed(seed)

    def demo():
        """
        给出接口使用示例
        """
        demo_str = '''
import clubear as cb
pathfile = '/clubear/data/single_files/airline.csv'
db = cb.subsample(pathfile) # initialize and specify the dataset path
db.seed(1) # set the random seed
num_lines = db.get_lines_num() # count lines of the dataset 
head = db.head() # get the first 5 lines
chunk = db.get_chunk(100) # get a chunk iteratively (input: chunk size)
sample = db.run() # addressing subsampling method
# parameters of addressing subsampling method:
# subsize: sample size (default: 1000)
# method: 'seq'- sequential subsampling; 'rand' - rand subsampling (default: 'rand')
sample = db.run(subsize=1000, method='seq') # sequential addressing subsampling
sample = db.run(subsize=1000, method='rand') # random addressing subsampling 
        '''
        print(demo_str)

    def __init__(self, original_data_path):
        """
        初始化方法
        """
        super(subsample, self).__init__()

        # 原始数据存放路径
        self.original_data_path = original_data_path


        # 数据是否OK（存在，为file）
        self.is_data_exits = False
        # 数据是否为空
        self.is_empty = False
        if os.path.exists(self.original_data_path) == False:
            print("subsample: [%s] does not exist! Please check the path." % self.original_data_path)
        elif os.path.isfile(self.original_data_path) == False:
            print("subsample: [%s] is not a file! Please check the path." % self.original_data_path)
        else:
            # 文件是否为空
            self.is_empty = self.is_file_empy()

            # 迭代读取器-准备
            # 先读取表头，并记录表头尾部的位置
            try:
                with open(self.original_data_path, 'r', errors='ignore', encoding='ISO-8859-1') as f:
                    f.seek(0, 0)
                    first_line = f.readline()
                    self.csv_header = first_line.split(',')
                    self.iterator_pos = max(len(first_line)-1,0)
            except:
                pass

            self.is_data_exits = True

    def is_file_empy(self):
        """
        判断文件是否为空
        """
        with open(self.original_data_path, 'r', errors='ignore', encoding='ISO-8859-1') as f:
            # 记录表头
            line = f.readline()
            header_str = line

            # 记录原始数据字节总长度
            f.seek(0, 2)
            file_num = f.tell()
        if len(header_str) == file_num:
            return True
        else:
            return False


    def head(self, nrow = 5):
        """
        展示数据前若干行
        """
        if self.is_data_exits:
            if self.is_empty:
                print("subsample.head: [%s] is empty." % self.original_data_path)
            else:
                reader = pd.read_csv(self.original_data_path, encoding='ISO-8859-1', iterator=True)
                chunk = reader.get_chunk(nrow) 
                #print(chunk)
                return chunk
        else:
            print("subsample.head: Please check the path.")

    def get_chunk(self, nrow = None):
        """
        分块顺序读取数据
        """
        if self.is_data_exits:
            if self.is_empty:
                print("subsample.get_chunk: [%s] is empty." % self.original_data_path)
            else:
                if nrow:
                    cnt = 0
                    sample = []
                    # 从指定位置开始读取数据
                    with open(self.original_data_path, 'r', errors='ignore', encoding='ISO-8859-1') as f:
                        f.seek(self.iterator_pos, 0)
                        # 跳到下行首部
                        line = f.readline()
     
                        # 读取指定行
                        while cnt < nrow and line:
                            line = f.readline()
                            sample.append(line.strip().split(','))
                            # 记录位移
                            self.iterator_pos = self.iterator_pos + len(line)
                            cnt += 1

                    try:
                        data = pd.DataFrame(sample, columns=self.csv_header)
                    except Exception:
                        data = None
                    return data
                else:
                    print("subsample.get_chunk: Please set the chunk size.")
        else:
            print("subsample.get_chunk: Please check the path.")

    def get_lines_num(self):
        """
        计算文件行数
        """
        if self.is_data_exits:
            if self.is_empty:
                print("subsample.get_lines_num: [%s] is empty." % self.original_data_path)
            else:
                count = 0
                try:
                    if self.is_data_exits:
                        _output = sys.stdout
                        with open(self.original_data_path, 'rb') as f:
                            while True:
                                buffer = f.read(8192*1024)
                                #print(buffer)
                                if not buffer:
                                    break
                                count += buffer.count('\n'.encode())

                                if count % 10 == 0:
                                    # 显示当前读取的行数
                                    _output.write('\rNumber of lines detected so far: %d' % (count-1))
                            _output.write('\rNumber of lines detected so far: %d\n' % (count-1))
                        # 将标准输出一次性刷新
                        _output.flush()

                        return count-1 # 统计内容行数，不记header那一行
                except:
                    print('subsample.get_lines_num: Please check the data path.')
        else:
            print("subsample.get_lines_num: Please check the path.")

    def run(self, **kwargs):
        """
        控制调用的subsample方法
        """
        if 'subsize' not in kwargs:
            # 默认抽样尺寸为1000
            subsize = 1000 
        else:
            subsize = kwargs['subsize']

        if 'method' not in kwargs:
            todo_method = 'rand'
        else:
            todo_method = kwargs['method']

        if todo_method == 'seq':
            d = self.seq_sample(subsize)
        else:
            d = self.rand_sample(subsize)
        return d


    def seq_sample(self, nrow):
        """
        指定行数，顺序寻址抽样
        """
        file_path = self.original_data_path
        if self.is_data_exits:
            if self.is_empty:
                print("subsample.seq_sample: [%s] is empty." % file_path)
            else:      
                if os.path.isfile(file_path) == True:
                    try:
                        cnt = 0
                        while cnt < nrow:
                            [d, cnt] = self.get_sample_from_sequential_data(file_path, nrow)
                        return d
                    except Exception as e:
                        print(e)
                        print("** Sampling Error! ** Please check your input parameter!")
                else:
                    print("subsample.seq_sample: [%s] is not a file." % file_path)
        else:
            print("subsample.seq_sample: Please check the path.")

    def get_sample_from_sequential_data(self, new_path, nrow):
        """
        顺序寻址抽样
        """

        # 获取CSV文件表头、字节总数
        [header, file_num] = self._get_file_info(new_path)
        num_header = len(header)

        # 产生随机起点
        pos = int(file_num * random.random())

        # 准备存放数据
        sample = []

        # 行计数器
        cnt = 0
        
        with open(new_path, 'r', encoding='ISO-8859-1') as f:

            f.seek(pos, 0)
            # 读取一行，使指针移动到下一行开头
            line = f.readline()
            
            # 读取指定行
            while cnt < nrow:
                line = f.readline()
                if not line:
                    f.seek(0, 0)
                    line = f.readline()
                else:
                    temp_sample = line.strip().split(',')
                    if len(temp_sample) == num_header and len(line)>0:
                        sample.append(temp_sample)
                        cnt += 1
         
        # 组合成 DataFrame
        d = pd.DataFrame(sample, columns = header)
        return [d, cnt]

    def _get_file_info(self, file_path):
        """
        确定文件总字节数及表头
        """
        # errors='ignore'
        with open(file_path, 'r', errors='ignore', encoding='ISO-8859-1') as f:
            # 记录表头
            line = f.readline()
            header = line.strip().split(',')

            # 记录原始数据字节总长度
            f.seek(0, 2)
            file_num = f.tell()
        return [header, file_num]


    def rand_sample(self, nrow, thread_num = 4):
        """
        指定行数，从原始数据抽样
        """

        new_path = self.original_data_path

        if os.path.exists(new_path) == True:
            if self.is_empty:
                print("subsample.rand_sample: [%s] is empty." % self.original_data_path)
            else:
                if os.path.isfile(new_path) == True:
                    try:
                        # 获取CSV文件表头、字节总数
                        [header, file_num] = self._get_file_info(new_path)

                        # 多进程通信，使用字典，以保持子进程结果的顺序
                        manager = Manager()
                        #return_list = manager.list([])
                        return_list = manager.dict()

                        # 进程列表
                        ps = []
                        # 分配每个子进程任务量
                        block_thread = self._assign_work_load(nrow, thread_num)

                        # 设置子进程种子
                        sub_seeds = []
                        for i in range(0, thread_num):
                            sub_seeds.append(int(random.random() * (2**32 - 1)))

                        # 设置子进程
                        for i in range(0, thread_num):
                            p = Process(target = self.get_sample_from_original_data,
                                args=(i, sub_seeds[i], new_path, header, file_num, block_thread[i], return_list))
                            ps.append(p)

                        # 启动子进程
                        for i in range(0, len(ps)):
                            ps[i].daemon = True
                            ps[i].start()  

                        for i in range(0, len(ps)):
                            ps[i].join()

                        # 按顺序合并子进程的结果
                        new_return_list = []
                        for i in range(0, thread_num):
                            new_return_list.append(return_list[i])

                        d = pd.concat(new_return_list, axis=0)
                        # 重新排序index
                        d = d.reset_index(drop=True)
                        return d
                    except Exception as e:
                        print(e)
                        print("subsample.rand_sample: Please check your input parameter!")
                else:
                    print("subsample.rand_sample: [%s] is not a file." % new_path)
        else:
            print("subsample.rand_sample: Please check the path.")

    def get_sample_from_original_data(self, sub_id, sub_seed, file_path, header, file_num, nrow, return_list):
        """
        指定行数，从原始数据抽样
        """
        # 强制设定子进程随机种子
        np.random.seed(sub_seed)

        # 存储已读取的行
        sample = []

        # header字段数量
        num_header = len(header)

        # 行计数器
        cnt = 0
        with open(file_path, 'r', encoding='ISO-8859-1') as f:
            while cnt < nrow: 
                try:   
                    #pos = int(random.random() * file_num)
                    pos = int(np.random.uniform(0.0, 1.0, 1) * file_num)
                    # 获取随机一行数据
                    f.seek(pos, 0)
                    # 读取一行，使指针移动到下一行开头
                    line = f.readline()
                    line = f.readline()
                    temp_sample = line.strip().split(',')
                    if len(temp_sample) == num_header and len(line)>0:
                        sample.append(temp_sample)
                        cnt = cnt + 1
                except:
                    pass
        # 组装为dataframe
        d = pd.DataFrame(sample, columns = header)  
        # 添加到列表中
        #return_list.append(d)
        return_list[sub_id] = d


    def _assign_work_load(self, all_num, thread_num):
        """
        分配多进程，每个进程的工作量
        """
        # 进程工作量列表
        block_thread = []

        # 每个进程抽样数量
        block = int(all_num / thread_num)
        for i in range(thread_num):
            block_thread.append(block)

        # 若剩余未分派的
        block_remain = int(all_num - block * thread_num)
        if block_remain > 0:
            block_thread[0] = block_thread[0] + block_remain
        return block_thread

    def rand_sample_single(self, nrow):
        """
        指定行数，从原始数据抽样(单进程)
        """

        new_path = self.original_data_path

        if os.path.exists(new_path) == True:
            if self.is_empty:
                print("subsample.rand_sample_single: [%s] is empty." % self.original_data_path)
            else:
                if os.path.isfile(new_path) == True:
                    try:
                        # 获取CSV文件表头、字节总数
                        [header, file_num] = self._get_file_info(new_path)
                        num_header = len(header)

                        # 存储已读取的行
                        sample = []
                        # 行计数器
                        cnt = 0
                        with open(new_path, 'r', encoding='ISO-8859-1') as f:
                            while cnt < nrow:
                                try:
                                    pos = int(random.random() * file_num)
                                    # 获取随机一行数据
                                    f.seek(pos, 0)
                                    # 读取一行，使指针移动到下一行开头
                                    line = f.readline()
                                    line = f.readline()
                                    temp_sample = line.strip().split(',')
                                    if len(temp_sample) == num_header and len(line)>0:
                                        sample.append(temp_sample)
                                        cnt = cnt + 1
                                except:
                                    pass
                        # 组装为dataframe
                        d = pd.DataFrame(sample, columns = header)  
                        return d
                    except:
                        print("subsample.rand_sample_single: Please check your input parameter!")
                else:
                    print("subsample.rand_sample_single: [%s] is not a file." % new_path)
        else:
            print("subsample.rand_sample_single: Please check the path.")

