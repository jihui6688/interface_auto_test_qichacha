''' 通过此文件可以获取接口参数、用户输入参数、预期
结果参数，将这些参数以元素为元祖的列表的形式返回'''
import requests
import unittest
import json
import time
from hashlib import md5
from  conf.setting import  *
import yaml

# 获取时间戳
def get_time_tup():
    """ :return: 13位精确到秒的时间戳
    """
    time_tup = str(int(time.time()))
    return time_tup

# md5加密
def set_md5(s):
    """
    :param s: 拼接的字符串
    :return: md5加密再转化为大写的字符串
    """
    new_md5 = md5()
    new_md5.update(s.encode(encoding='utf-8'))
    s_md5 = new_md5.hexdigest().upper()
    return  s_md5

# 设置请求头
def get_headers(key, screat_key):
    """
    :param key: 我的key
    :param screat_key: 我的密钥
    :return: 请求头
    """
    headers = dict()
    token = key + get_time_tup() + screat_key
    headers["Token"] = set_md5(token)
    headers["Timespan"] = get_time_tup()
    return headers
# 读取 yaml 文件，从中提取参数，放入
with open(yaml_path,'r+',encoding='utf-8') as f:
    y = list(yaml.load_all(f))
# 所有接口请求参数中的公共参数
common_data = y[0]['common_parameter']
print("common_data is :"+str(common_data))
# 获取 key 和 screat_key 用来得到请求头
key = y[0]['header_parameter']['key']
print("key is :"+key)
screat_key = y[0]['header_parameter']['screat_key']
print("screat_key is :"+screat_key)
# list_data 提供测试用例的参数化，初始值为空
list_data = []
''' 读取 yaml 文件后，返回一个列表，
列表中第二个参数为参数用例相关的参数 '''
case_list = y[1]
# index 是用来表示测试用例的编号
index = 1
# 通过 for 循环进一步读取 yaml 文件中的参数
for k in case_list:
	# 获取接口的 url 参数
    URL = k['base_url']
    # 通过 for 循环读取多个用户输入的参数
    for i in range(0, k['test_case'].__len__()):
    	# 获取用户输入参数
        user_data = k['test_case'][i]['user_input_parameter']
        # 获取接预期的 http 状态码
        status_code =str( k['test_case'][i]['expect_status_code'])
        # 将用户输入的参数与接口的通用参数合并（将两个字典合并为一个字典）
        data = dict(user_data, **common_data)
        # 获取请求头参数
        headers_data = get_headers(key, screat_key)
        # 用例的编号
        index_str = str(index)
        ''' 将获取的参数：用例编号、URL、请求头参数、请求参数、http状态码
        这 5 个参数赋值给元祖，用来进行接口的参数化 '''
        tuple_data = index_str, URL, headers_data, data,status_code
        # 将元祖添加到列表中，每一个元祖对应一个测试用例的参数
        list_data.append(tuple_data)
        # 用例编号加一
        index = index + 1
# 打印得到的请求参数
print("list data is :"+str(list_data))