# 此文件用来将生成的测试报告以邮件的方式发送给指定的接收人
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from conf import setting
import os

class SendEmail:
    def __init__(self,receivers = None):
        self.mail_host = "smtp.163.com"  # 设置服务器
        self.mail_user = "18*********@163.com"  # 用户名
        self.mail_pass = "********"  # 密令/密码
        # 发送者邮箱
        self.sender = '18*********@163.com'
        if receivers:
            self.receivers = receivers
        else:
            # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
            self.receivers = ['10********@qq.com',"1********@qq.com"]

    def get_report_file(self,report_file):
        """获取最近一次测试报告"""
        report_path = os.path.join(setting.report_dir,report_file)
        print(report_path)
        with open(report_path,'rb') as f:
            mail_content = f.read()
        return mail_content

    def send_email(self,report_file):
        content = self.get_report_file(report_file)
        # 邮件内容
        message = MIMEText(content, _subtype='html', _charset='utf-8') 
        subject = '企查查大数据接口_自动化测试报告'
        # 邮件主题
        message['Subject'] = Header(subject, 'utf-8')  
        # 发送人，必填，邮箱格式
        message['From'] = self.sender  
        # 收件人，必填，邮箱格式
        message['To'] = ";".join(self.receivers)  
        server = smtplib.SMTP()
        # server.connect(self.mail_host, 25)  
        # 连接服务器
        server = smtplib.SMTP_SSL(self.mail_host, 465)
        # 登录
        server.login(self.mail_user, self.mail_pass) 
        try:
            server.sendmail(self.sender, self.receivers, message.as_string())
            print('发送成功')
        except smtplib.SMTPException as e:
            print("Error: 无法发送邮件")
        server.close()

