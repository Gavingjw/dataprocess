# dataprocess

需求；对100G的车辆运行数据进行筛选排序，然后输出每辆车按照时间顺序进行排序的文件，
解决方案：
1. 用户提供的脚本能够实现小量数据的处理，但对大量的数据是无法进行处理的，需要重新修改解决方案
2. 最后形成通过一次一行一分类的方法，当累计的数据达到一定数量后对数据进行写入操作，成功完成用户需求。


# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:36:48 2019

@author: vsjlv
"""
import pandas as pd
#此部分代码按标签排序
df=pd.read_csv('导入地址\文件名.csv')
#填写地址及文件名
df.dropna(axis=0,subset=['create_date'])
#若时间字段中有空白字段，则剔除此行数据
#df.dropna(axis=0,how='any')
df2=df.sort_values(by=['版本号','vin','create_date'])
#按照版本号和VIN和时间排序
df2.to_csv('导出地址\文件名.csv')
#导出处理后的csv，并命名



