#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.utils import shuffle as sk_shuffle
import random
import os
import sys
import shutil
import time
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')


class shuffle(object):

    def demo():
        """
        给出接口使用示例
        """
        demo_str = '''
pathfile = '/clubear/data/single_files/airline.csv'
shuffle=CluBear.shuffle(pathfile)
shuffle.go()        '''
        print(demo_str)

    def __init__(self, original_data_path):
        """
        初始化方法
        """
        super(shuffle, self).__init__()

        # 原始数据存放路径
        self.original_data_path = original_data_path

        # shuffle后的文件存放路径，默认为原始路径
        # 若为windows路径，须将\替换为/
        _convert_original_data_path = re.sub(r'\\', '/', original_data_path)
        file_pat = re.compile(r'/([^/]*)\.csv')
        file_name_middles = file_pat.findall('/'+_convert_original_data_path)
        self.shuffled_path = './%s.csv.shuffle' % file_name_middles[0]

        # 判断原始文件路径是否存在
        if os.path.exists(self.original_data_path) == False:
            print("Error: [%s] does not exist! Please check the path." %
                  self.original_data_path)
            self.is_data_exits = False
        else:
            self.is_data_exits = True

    def go(self, **kwargs):
        """
        执行shuffle操作
        根据输入的参数（shuffle方式）不同，调用不同的方法进行shuffle
        """
        if 'method' not in kwargs:
            # 若未指定shuffle方式
            self.shuffle_divide_conque(None, 200)
        else:
            # 若指定采用 divide-conque 方式进行shuffle
            if kwargs['method'] == 'divide-conque':
                if 'output_path' in kwargs:
                    new_path = kwargs['output_path']
                else:
                    new_path = None
                if 'cache_file_num' in kwargs:
                    cache_file_num = kwargs['cache_file_num']
                else:
                    cache_file_num = 200
                self.shuffle_divide_conque(new_path, cache_file_num)
            # 若采用 XX 方式进行shuffle
            elif kwargs['method'] == 'XX':
                pass
    def shuffle_divide_conque(self, new_path=None, cache_file_num=200):
        """
        随机排序方法
        """
        # 若没有指定存放位置，则将shuffle后文件放到默认位置
        if new_path == None:
            new_path = self.shuffled_path
        else:
            self.shuffled_path = new_path

        # 指定工作文件夹，保存中间文件
        self.work_space = './_CluBear_file/'
        # 日志
        self.log_path = self.work_space + '_log.txt'

        # 禁止将shuffle后文件路径设置为与原始文件路径相同
        if new_path == self.original_data_path:
            print("Warning: Are you sure to rewrite the original file?")
        else:
            if self.is_data_exits:
                #print('[ Shuffling ]')
                t0_shuffle = time.time()
                _output = sys.stdout

                # 创建中间文件文件夹
                if not os.path.exists(self.work_space):
                    os.mkdir(self.work_space)

                self._log('[ Shuffling ] %s' % self._now_time())

                # 创建文件夹，保存排序的中间文件
                self.cache_fold = self.work_space + '_cache/'
                # 刷新cache文件夹
                if os.path.exists(self.cache_fold):
                    shutil.rmtree(self.cache_fold)
                os.mkdir(self.cache_fold)

                # [step-1].把原数据每一行随机分配给若干个cache
                t0 = time.time()
                header_str = self._shuffle_assign(cache_file_num, _output)
                t1 = time.time()
                self._log('** shuffle - cache assignment: %.2fs' % (t1 - t0))

                # [step-2].对每个cache，打乱内部顺序
                t0 = time.time()
                #print('\n[ Shuffling Step-2/3]')

                for i in range(0, cache_file_num):
                    d = self._input(self.cache_fold + str(i))
                    # 随机排序
                    d = sk_shuffle(d)
                    self._output(d, self.cache_fold + str(i))

                    status = 100 * (i+1) / float(cache_file_num)
                    _output.write(
                        '\rShuffle stage (2/3) accomplished: %.2f %%   ' % (status))

                # 将标准输出一次性刷新
                # _output.flush()
                # """

                t1 = time.time()
                self._log('** shuffle - cache shuffling: %.2fs' % (t1 - t0))

                # 拼接cache，组成最终文件
                t0 = time.time()
                #print('\n[ Shuffling Step-3/3]')

                # 先对所有cache，产生一个随机排序
                concat_order = list(pd.Series(range(cache_file_num)).sample(
                    cache_file_num, replace=False))

                # 刷新 new_path 指定的文件
                with open(new_path, 'w', encoding='ISO-8859-1') as f:
                    f.write(header_str)

                with open(self.original_data_path, 'r', encoding='ISO-8859-1', errors='ignore') as of:

                    with open(new_path, 'a', encoding='ISO-8859-1') as f:
                        # 按照随机顺序，写入cache内容
                        for i in range(0, len(concat_order)):
                            with open(self.cache_fold + str(concat_order[i]), 'r') as fc:
                                line = fc.readline()
                                while line:
                                    # 当前读取的line，只是一个行index
                                    line = fc.readline()
                                    # 利用行index寻找原始文件里那一行
                                    try:
                                        of.seek(int(line), 0)
                                        original_line = of.readline()
                                        if len(original_line) > 0:
                                            if '\n' not in original_line:
                                                original_line = original_line + '\n'
                                            f.write(original_line)
                                    except:
                                        pass
                            # 写入完毕后，删除cache文件
                            os.remove(self.cache_fold + str(concat_order[i]))

                            status = 100 * (i+1) / float(cache_file_num)
                            _output.write(
                                '\rShuffle stage (3/3) accomplished: %.2f %%   ' % (status))

                t1_shuffle = time.time()
                _output.write('\rShuffling accomplished (%s) and shuffled file is generated as: %s \n' % (
                    self._count_time(t1_shuffle - t0_shuffle), self.shuffled_path))

                # 将标准输出一次性刷新
                _output.flush()

                # 最终删除cache文件夹
                shutil.rmtree(self.cache_fold)

                t1 = time.time()
                self._log('** shuffle - cache concating: %.2fs' % (t1 - t0))
                #print("\nShuffling finished!")

                # 0411增加：删除工作文件夹
                shutil.rmtree(self.work_space)

    """
    * 内部辅助方法
    """

    def _input(self, input_path):
        """
        获取csv数据方法
        """
        d = pd.read_csv(input_path, encoding='ISO-8859-1')
        return d

    def _output(self, data, output_path):
        """
        写出csv数据方法
        """
        data.to_csv(output_path, encoding='ISO-8859-1', index=False)

    def _shuffle_assign(self, cache_file_num, _output):
        """
        打乱原始文件排序，打散成若干个文件
        """

        # 获取标准输出
        #_output = sys.stdout
        # 行计数器
        cnt = 0
        with open(self.original_data_path, 'r', encoding='ISO-8859-1', errors='ignore') as f:
            # 记录原始数据字节总长度
            f.seek(0, 2)
            file_num = f.tell()

            # 单行大概长度
            f.seek(0, 0)
            line = f.readline()
            line = f.readline()
            byte_line = len(line)

            # 估计行数
            line_num_est = int(file_num / byte_line)
            #line_num_est = self.get_lines_num()
            # print(line_num_est)
            # 刷新频率
            flush = int(max(line_num_est / 1000, 10))

        with open(self.original_data_path, 'r', encoding='ISO-8859-1', errors='ignore') as f:
            # 头一行为表头
            line = f.readline()
            header_str = line
            cul_pos = len(line)

            # 创建多个cache文件
            cache_list = []
            for i in range(0, cache_file_num):
                fc = open(self.cache_fold + str(i), 'w')
                fc.write('row_index\n')
                cache_list.append(fc)

            while line:  # cnt < 100:
                # 读取一行
                line = f.readline()
                # 随机放入一个cache
                cache_no = int(random.random() * cache_file_num)

                """
                修改！不再写入一行，而是写入行的开头位置
                """
                # 追加写入某个cache
                cache_list[cache_no].write('%d\n' % cul_pos)
                # 更新指针位置
                cul_pos = cul_pos + len(line)

                # 记录已经处理的行数
                cnt = cnt + 1
                if cnt % flush == 0:
                    # 估计当前进度
                    status = min(100 * (cul_pos+1) / float(file_num), 100)
                    _output.write(
                        '\rShuffle stage (1/3) accomplished: %.2f %%' % status)
            _output.write('\rShuffle stage (1/3) accomplished: 100.00 %')

        # 将标准输出一次性刷新
        # _output.flush()

        # 关闭所有cache文件
        for i in range(0, cache_file_num):
            cache_list[i].close()
        return header_str

    def _log(self, info):
        """
        记录日志
        """
        with open(self.log_path, 'a') as f:
            f.write(info + '\n')

    def _now_time(self):
        """
        当前时间
        """
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def _count_time(self, _t):
        """
        整理时间格式
        """
        _hour = int(_t/3600)
        _t = _t - 3600*_hour
        _min = int(_t/60)
        _sec = _t - 60*_min
        time_str = ''
        if _hour > 0:
            time_str = time_str + str(_hour) + 'h'
        if _min > 0:
            time_str = time_str + str(_min) + 'm'

        if _hour > 0 or _min > 0:
            time_str = time_str + str(int(_sec)) + 's'
        else:
            time_str = '%.2fs' % _sec
        return time_str
