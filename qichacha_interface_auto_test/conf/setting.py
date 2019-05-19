'''
此文件用来获取文件或目录的路径
'''
import os
# 项目的根路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 测试报告的路径
report_dir = os.path.join(base_dir,"report")
# 测试用例目录
test_dir = os.path.join(base_dir,'case')
# yaml 文件的路径
yaml_path = os.path.join(base_dir,'conf','conf.yal')

if __name__ == '__main__':
    print(report_dir)
    print(base_dir)
    print(test_dir) 
    print(yaml_path)