import pymysql

def create_connection():
       connection = pymysql.connect(
           host='localhost',
           user='root',
           password='1234',
           database='FB'
       )
       return connection
