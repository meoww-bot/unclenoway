#!/usr/bin/env python
# coding:utf-8

import json
import requests
import os
import time
import argparse
import sqlite3

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

db = 'data.db'

def req(number):
    s = requests.Session()
    url = 'http://118.190.174.130:3101/lostFound/{}'.format(str(20*number))
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E238 Safari/601.1', 'Content-Type': 'application/x-www-form-urlencoded'}
    print '[*] payload sending ...{}'.format(str(20*number))
    r = s.get(url, headers=headers)
    
    data = json.loads(r.text)
    if not os.path.exists(db):
        init_db()

    for n in data:
        _id = n["_id"]
        postNumber = n["postNumber"]
        lostDate = n["lostDate"]
        wechat = n["wechat"]
        title = n["title"]
        article = n["article"]
        question = n["question"]
        posterId = n["posterId"]
        likes = n["likes"]
        postDate = n["postDate"]
        isFound = n["isFound"]
        status = n["status"]

        # if 
        insert(_id, postNumber, lostDate, wechat,title,article,question,posterId,likes,postDate,isFound,status)
        print 'insert ok, postnumber:{} '.format(postNumber)


def init_db():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    #sqlite3.Warning: You can only execute one statement at a time.
    SQL_INIT1 = '''PRAGMA foreign_keys = FALSE;'''
    SQL_INIT2 = '''
CREATE TABLE IF NOT EXISTS lostFound (
	_id VARCHAR(2000) NOT NULL,
	postNumber VARCHAR(20) NOT NULL,
	lostDate VARCHAR(20) NOT NULL,
	wechat VARCHAR(2000) NOT NULL,
	title VARCHAR(2000) NOT NULL,
    article VARCHAR(2000) NOT NULL,
    question VARCHAR(2000) NOT NULL,
    posterId VARCHAR(2000) NOT NULL,
    likes VARCHAR(2000) NOT NULL,
    postDate VARCHAR(2000) NOT NULL,
    isFound VARCHAR(2000) NOT NULL,
    status VARCHAR(2000) NOT NULL,
	PRIMARY KEY (postNumber)
);'''
    SQL_INIT3 = '''PRAGMA foreign_keys = TRUE;'''
    
    cursor.execute(SQL_INIT1)
    cursor.execute(SQL_INIT2)
    cursor.execute(SQL_INIT3)
    print "database init success"
    cursor.close()
    conn.commit()
    conn.close()

# def search(question):
#     conn = sqlite3.connect('data.db')
#     sql = "select * from questions where quiz LIKE '{}'"
#     answer = conn.execute(sql.format(question)).fetchall()[-1][-1]
#     conn.close()
#     return answer

def _decode_utf8(aStr):
    return aStr.encode('utf-8','ignore').decode('utf-8')

def insert(_id, postNumber, lostDate, wechat,title,article,question,posterId,likes,postDate,isFound,status):
    conn = sqlite3.connect('data.db')
    #sql = "INSERT INTO `lostFound`(`_id`, `postNumber`, `lostDate`, `wechat`,`title`,`article`,`question`,`posterId`,`likes`,`postDate`,`isFound`,`status`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');"
    sql = "INSERT INTO `lostFound`(`_id`, `postNumber`, `lostDate`, `wechat`,`title`,`article`,`question`,`posterId`,`likes`,`postDate`,`isFound`,`status`) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
    c = conn.cursor()
    insert_data = map(_decode_utf8,(_id, postNumber, lostDate, wechat,title,article,question,posterId,likes,postDate,isFound,status))
    r = c.execute(sql,insert_data)
    conn.commit()
    conn.close()


def update(question, answer_no):
    conn = sqlite3.connect('data.db')
    sql = "select `options` from `questions` where `quiz` = '{}'"
    c = conn.cursor()
    options = c.execute(sql.format(question)).fetchall()[-1][-1]
    answer = options.strip('[').strip(']').split()[answer_no - 1]
    sql = "UPDATE `questions` SET `answer`='{}' WHERE `quiz`='{}';"
    r = c.execute(sql.format(answer, question))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    for x in xrange(1967):#39340/88467
        req(x)
