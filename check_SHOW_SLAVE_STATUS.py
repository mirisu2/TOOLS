#!/usr/bin/python3
import pymysql.cursors
import requests
import os


url = 'http://notify.h744.host/api/v1/telegram'
headers = {
    'Content-Type': 'application/json',
    'X-NOTIFY-API-Key': os.environ['X_NOTIFY_API_Key']
    }
payload = {
    'id': os.environ['TELEGRAM_ID'],
    'text': 'db2.pi-telecom says check SHOW_SLAVE_STATUS'
    }

con = pymysql.connect(host='localhost',
    user=os.environ['MYSQL_USER'],
    password=os.environ['MYSQL_PASSW'],
    db='mysql',
    cursorclass=pymysql.cursors.DictCursor)

try:
    with con.cursor() as cursor:
        cursor.execute('SHOW SLAVE STATUS')
        output = cursor.fetchone()
        if output['Slave_IO_State'] != 'Waiting for master to send event' and output['Slave_IO_Running'] != 'Yes' and output['Slave_SQL_Running'] != 'Yes':
            requests.get(url, json=payload, headers=headers)
finally:
    con.close()
