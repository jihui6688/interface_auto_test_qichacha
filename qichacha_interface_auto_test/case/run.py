# 此文件是项目执行的入口
import unittest
from util.HTMLTestRunner import HTMLTestRunner
import time
from conf.setting import report_dir
from conf.setting import test_dir
from  util.send_email import SendEmail

# 指定测试用例 的路径
discover = unittest.defaultTestLoader.discover(test_dir,pattern='test_case.py')
now=time.strftime('%Y_%m_%d_%H_%M_%S')
# 指定生成的测试报告的文件名
report_name=report_dir+'/'+now+' test_report.html'
# 将测试结果写入测试报告
with open (report_name,'wb') as f:
    runner = HTMLTestRunner(stream=f,title='Vincent Qichacha API Test Report',description=' Qichacha API Test Report By Vincent ',verbosity=2)
    runner.run(discover)
# 将测试报告发送到指定的邮箱
send_email_report = SendEmail()
send_email_report.send_email(report_name)