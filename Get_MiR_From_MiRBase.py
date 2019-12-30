#!/usr/bin/env python3
# coding: utf-8
# Author: Devin561
# E-Mail: zengzhen561@163.com

import re
import os
import sys


def get_miR(file, num):
    """从miRBase本地数据库中搜索对应的编号，生成一个新的fasta文件"""
    outfile = open(os.path.basename(file).split('.')[0] + "_{0}.".format(num) + os.path.basename(file).split('.')[1], 'w')
    # 新建一个文件夹，名字根据输入的编号确定
    dict = {}
    num = str(num)
    with open(file, 'r') as fasta:
        # 打开文件
        for line in fasta:
            # 读取每一行
            if line.startswith('>'):
                # 以'>'开头的为基因名，将名字存为name的变量中
                name = line.lstrip('>').strip()
                dict[name] = ''
            else:
                # 如果开头不是'>',则这一行应该就是序列了，将这一行归类到上面提到的名字中
                dict[name] += line.strip()
                RE = re.search('miR' + num + r'\D', name)
                # 只筛选植物的，搜索名字中带有miR***的，如miR399
                if RE:
                    outfile.write('>' + name + '\n' + str(''.join(dict[name])) + '\n')
                    # 输出文件
                else:
                    pass
    outfile.close()


if __name__ == '__main__':
    get_miR('./mature.fa', sys.argv[1])
