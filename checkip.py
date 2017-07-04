import subprocess
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def sendmail(ip):
    host = 'smtp.126.com'
    port = 465
    sender = 'test@126.com'
    receivers = ['test2@126.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    message = MIMEText(ip, 'plain', 'utf-8')
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['subject'] = 'ip变更'
#     message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(host, port)
#         smtpObj.ehlo()
#         smtpObj.connect(host, port)
        smtpObj.login(sender, '123456')
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.close()
        print("邮件发送成功")
    except smtplib.SMTPException as s:
        print(s)
        print("Error: 无法发送邮件")


def checkip():
    fp = subprocess.Popen(
        ['curl ipinfo.io'], shell=True, stdout=subprocess.PIPE)
    data = fp.communicate()
    d = data[0].decode('utf8')
    dec = json.loads(d)
    with open('/tmp/checkip.txt', 'r') as f:
        line = f.readline()
        line = line.strip('\n')
        f.close()
        print("current dns ip is" + line)
        if line != dec['ip']:
            print('ip changed, before: {0}, after:{1}'.format(line, dec['ip']))
            msg = 'before:' + line + ' after:' + dec['ip']
            sendmail(msg)
            subprocess.call(
                'echo ' + dec['ip'] + ' > /tmp/checkip.txt', shell=True)
        else:
            print("same ip do nothing")
checkip()
