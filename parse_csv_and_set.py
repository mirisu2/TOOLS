# pip install pymysql
import pymysql
# pip install pyyaml
import yaml
import csv
import time


start = time.time()
sets = yaml.safe_load(open('config.yaml'))
db = {
    'host': sets['mysql_clients']['DB_HOST'],
    'user': sets['mysql_clients']['DB_USER'],
    'password': sets['mysql_clients']['DB_PASS'],
    'db': sets['mysql_clients']['DB_NAME']
}


def connect():
    connector = pymysql.Connect(host=db['host'], user=db['user'], password=db['password'], db=db['db'],
                           charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    return connector


with open('input.csv', 'r') as csvfile:
    r = csv.reader(csvfile, delimiter='|')
    try:
        conn = connect()
        print("Connected")
        i = 0
        with conn.cursor() as cursor:
            for row in r:
                cursor.execute('UPDATE dognet SET statusid=4 WHERE mnemo=%s', row[1].strip())
                conn.commit()
                i += cursor.rowcount
            print("Number of rows updated: %d" % i)
    except pymysql.err.OperationalError as e:
        print(e)
    else:
        conn.close()
        print("Disconnected")

end = time.time()
print('Execution time:', round(end - start, 2), 'sec')