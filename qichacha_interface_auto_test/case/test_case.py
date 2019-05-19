import requests
import unittest
import json
import time
from hashlib import md5
from  conf.setting import  *
import yaml
from util.get_request_parameters import list_data
import unittest
# 使用 nose-parameterized 对Python单元测试框架实现参数化
from parameterized import parameterized

''' 通过 util.get_request_parameters 
    模块返回的元祖列表 list_data，实现参数化 ，
    元祖列表 list_data 中的每一个元祖包含 5 个元素，
    第一个是 用例的编号，中间三个分别是 请求的 url、请求头、
   请求的参数，最后一个元素是测试用例的期望结果，期望结果
  我使用的是响应参数的 http 状态码，也可以是其他的响应参数 '''
class TestQichacha(unittest.TestCase):
    @parameterized.expand(
            list_data
    )
    
    def test(self, name, a, b, c,expect_status_code):
        s = requests.get(url=a, headers=b, params=c)
        # print(s.url)
        print("s.text :"+ s.text)
        result = s.json()
        # 打印实际的 http 状态码
        print("status code is : "+ result["Status"])
        # 断言实际的 http 状态码和预期结果的 http 状态码相等
        self.assertEqual(expect_status_code,result["Status"])

if __name__ == '__main__':
    unittest.main(verbosity=3)
