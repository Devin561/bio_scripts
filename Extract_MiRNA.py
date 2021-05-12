#!/usr/bin/env python3
# coding:utf-8
# Author: Devin561
# E-Mail: zengzhen561@163.com

import re
import sys
import os

def ly(file):
    id_line_num = [0]
    get_n = [0]
    line_out_num = []
    lines_num = []
    # out = open('output_file', 'w')
    out = open(os.path.basename(file).split('.')[0] + "_1." + os.path.basename(file).split('.')[1], 'w')
    # 根据输入文件来命名输出文件，在前缀前加 _1
    with open(file, 'r') as ly:
        for line_num, line in enumerate(ly):
            # 打开文件，line_num为读取的行，line为每一行的内容
            lines_num.append(line_num)
            # 将每一行的行号存入列表lines_num
            if re.match('>', line):
                id_line_num.append(line_num)
                # 如果每一行开头是">"，那么将行号放入数组id_line_num
                if id_line_num[-1] - id_line_num[-2] > 2:
                    get_n.append(id_line_num[-2])
                    # 如果两个">"之间间隔两行以上，将行号放入数组get_n
                    if get_n[-1] == 0:
                        # 考虑第一个">"就有两行以上
                        for j in range(get_n[-1], id_line_num[-1]):
                            line_out_num.append(j)
                    for i in range(get_n[-1], id_line_num[id_line_num.index(get_n[-1]) + 1]):
                        # 取有两行以上的行的">"行号及其下面所包含的行的行号，放入line_out_num；index是下一个">"的行号
                        line_out_num.append(i)
        # print(lines_num)
        if lines_num[-1] - id_line_num[-1] > 1 and lines_num[-1] - id_line_num[-2] > 3:
            # 考虑最后一个">"有两行以上
            for k in range(id_line_num[-1], lines_num[-1] + 1):
                line_out_num.append(k)

    new = open(file, 'r').readlines()
    for n in line_out_num:
        # 根据得到的行号，提取行
        out.write(new[n])

    out.close()
    print('已生成文件：{0}'.format(os.path.basename(file).split('.')[0] + "_1." + os.path.basename(file).split('.')[1]))


if __name__ == '__main__':
    ly(sys.argv[1])
