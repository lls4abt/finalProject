#!/usr/bin/env python3

# Lilleth Snavely (lls4abt)

import time
import requests
import pymysql
from datetime import datetime

DB_NAME = 'ds3002_finalProject'
HOST = 'ds3002-finalproject.cx4668glfjli.us-east-1.rds.amazonaws.com'
USER = 'ds3002_lls4abt'
PASS = 'ds3002finalProject'

mydb = pymysql.connect(
    host=HOST,
    user=USER,
    passwd=PASS,
    db="ds3002_finalProject"
)

mycursor = mydb.cursor()

stmt = "SHOW TABLES LIKE '%s' " % ('%' + str("apilog") + '%')
mycursor.execute(stmt)
result = mycursor.fetchone()

if result:
    deleteTable = f"DROP TABLE apilog"
    mycursor.execute(deleteTable)

createTable = f"CREATE TABLE apilog (Logkey int NOT NULL, Logtime varchar(10) DEFAULT NULL,Rfactor int DEFAULT NULL,Rpi float DEFAULT NULL, Rtime varchar(45) DEFAULT NULL, PRIMARY KEY(Logkey))"

mycursor.execute(createTable)


while datetime.now().minute != 0:
    time.sleep(.1)

starttime = time.time()
endtime = starttime + 3600

def insertEntry(theTime: time):
    logtimestamp = theTime
    logtime = time.strftime("%H:%M:%S", time.localtime(logtimestamp))
    logkey = int(logtimestamp)
    response = requests.get("https://4feaquhyai.execute-api.us-east-1.amazonaws.com/api/pi")
    rjson = response.json()
    rfactor = rjson['factor']
    rpi = rjson['pi']
    rtime = rjson['time']
    sql = "INSERT INTO apilog (logkey,logtime,rfactor,rpi,rtime) VALUES ("
    sql = sql + str(logkey) + ",'" + logtime + "'," + str(rfactor) + "," + str(rpi)
    sql = sql + ",'" + str(rtime) + "')"
    mycursor.execute(sql)

while time.time() <= endtime:
    insertEntry(time.time())
    mydb.commit()
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
