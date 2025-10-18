import mysql.connector
import mysql.connector.errorcode as errorcode
#import logging
from config import config

def MYSQL_Connect():
    try:
        cnx = mysql.connector.connect(**config)#unpacking config
        print("Connection successful")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()
        
MYSQL_Connect()
        
def MYSQL_CreateTable():
    pass