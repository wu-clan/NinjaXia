#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from backend.common.log import log
from backend.crud.crud_sys.crud_sys_email import crud_sender, crud_receiver


def send_test_report(subject, content):
    """
    发送测试报告

    :param subject: 主题
    :param content: 内容
    :return:
    """
    # 发送数据准备
    smtp_server = crud_sender.get_smtp_server()
    smtp_port = crud_sender.get_smtp_port()
    sender_email = crud_sender.get_sender_email()
    sender_password = crud_sender.get_sender_password()
    is_ssl = crud_sender.get_is_ssl()
    to = []
    for _ in crud_receiver.get_all_receiver():
        to.append(_.email)

    # 发送内容准备
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
    msg['From'] = sender_email
    msg.attach(MIMEText(content, 'html', 'utf-8'))

    # 发送
    smtp = None
    try:
        if is_ssl:
            smtp = smtplib.SMTP_SSL(host=smtp_server, port=smtp_port)
        else:
            smtp = smtplib.SMTP(host=smtp_server, port=smtp_port)
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, to, msg.as_string())
    except Exception as e:
        log.error(f'发送邮件失败，错误信息：{e}')
        raise Exception(f'发送邮件失败，错误信息：{e}')
    else:
        log.info('发送邮件成功')
    finally:
        smtp.quit()
