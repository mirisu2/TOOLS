#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from datetime import datetime
import shutil
import smtplib
from configparser import ConfigParser


def send_email(subject, body_text, emails):
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "email.ini")

    if os.path.exists(config_path):
        cfg = ConfigParser()
        cfg.read(config_path)
    else:
        sys.exit(1)

    host = cfg.get("smtp", "server")
    port = cfg.get("smtp", "port")
    from_addr = cfg.get("smtp", "from_addr")
    passwd = cfg.get("smtp", "passwd")

    body = "\r\n".join((
        "From: %s" % from_addr,
        "To: %s" % ', '.join(emails),
        "Subject: %s" % subject ,
        "",
        body_text
    ))

    server = smtplib.SMTP(host, port)
    server.login(from_addr, passwd)
    server.sendmail(from_addr, emails, body)
    server.quit()


if __name__ == '__main__':
    emails = ['admin@pi-tele.ru']
    subject = '[RELAY-SRV] Everyday backup'
    d = datetime.today()
    year, month, day = d.year, d.month, d.day

    body_text = 'Starting backup: {}\n'.format(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

    disk = shutil.disk_usage('/')
    total = round(disk.total/1024/1024/1024)
    used = round(disk.used/1024/1024/1024)
    free = round(disk.free/1024/1024/1024)
    body_text += 'Disk usage: TOTAL({}G), USED({}G), FREE({}G)\n'.format(total, used, free)

    # Backup system
    etc = shutil.make_archive('/tmp/{0}-{1}/etc_{0}-{1}'.format(year, month), 'tar', '/etc')
    root = shutil.make_archive('/tmp/{0}-{1}/root_{0}-{1}'.format(year, month), 'tar', '/root')
    opt = shutil.make_archive('/tmp/{0}-{1}/opt_{0}-{1}'.format(year, month), 'tar', '/opt')

    # Backup IredMail DBs
    os.system('/bin/bash /var/vmail/backup/backup_mysql.sh')
    mysql_backup_path = '/tmp/mysql/{}/{:02}/{:02}'.format(year, month, day)
    mysql = shutil.make_archive('/tmp/mysql/{0}/{1}/mysql_{0}-{1}'.format(year, month), 'tar', mysql_backup_path)

    # Put together all archives
    backup_relay = shutil.make_archive('/tmp/backup_relay_{0}-{1}-{2}'.format(year, month, day), 'gztar', '/tmp/{0}-{1}'.format(year, month))
    file_size = os.path.getsize(backup_relay)
    body_text += 'File: {}\n'.format(backup_relay)
    body_text += 'File size: {}M\n'.format(round(file_size/1024/1024))

    # cp = os.system('sshpass -p {} scp -o StrictHostKeyChecking=no {} {}@{}'.format(os.environ.get('BACKUP_PASS'), backup_relay, os.environ.get('BACKUP_USER'), '192.168.2.18:/E:/SRV_RELAY'))
    #cp = os.system('sshpass -p zZ000000 scp -o StrictHostKeyChecking=no {} backuper@192.168.2.18:/E:/SRV_RELAY'.format(backup_relay))
    cp = os.system('sshpass -p Zz000000 scp -o StrictHostKeyChecking=no {} backuper@192.168.2.19:/D:/srv_relay'.format(backup_relay))


    if cp == 0:
        os.system('rm -r -f /tmp/{}-{}'.format(year, month))
        os.system('rm -r -f /tmp/mysql')
        os.system('rm -r -f {}'.format(backup_relay))
        body_text += 'Backup completed: {}'.format(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        body_text += 'ERROR: Backup was not completed!'

    # Send log to email
    send_email(subject, body_text, emails)
