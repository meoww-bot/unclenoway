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
        postNumber = n["postNumber"] #int
        lostDate = n["lostDate"]
        wechat = n["wechat"]  #custom-defined
        title = n["title"] #custom-defined
        article = n["article"] #custom-defined
        question = n["question"] #custom-defined
        posterId = n["posterId"]
        likes = n["likes"] #int
        postDate = n["postDate"] #int
        isFound = n["isFound"] 
        status = n["status"] #int

        
        # insert_data = map(clear_dirtystr,(_id, postNumber, lostDate, wechat,title,article,question,posterId,likes,postDate,isFound,status))
        insert(_id, postNumber, lostDate, clear_dirtystr(wechat),clear_dirtystr(title),clear_dirtystr(article),clear_dirtystr(question),posterId,likes,postDate,isFound,status)
        print 'insert ok, postnumber:{} '.format(postNumber)

        if postNumber == 1:
            print '[*] finish!'
            sys.exit(1)


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
	PRIMARY KEY (_id)
);'''
    SQL_INIT3 = '''PRAGMA foreign_keys = TRUE;'''
    
    cursor.execute(SQL_INIT1)
    cursor.execute(SQL_INIT2)#77648 dunpliate orz
    cursor.execute(SQL_INIT3)
    print "[*]database init success"
    cursor.close()
    conn.commit()
    conn.close()

# def search(question):
#     conn = sqlite3.connect(db)
#     sql = "select * from questions where quiz LIKE '{}'"
#     answer = conn.execute(sql.format(question)).fetchall()[-1][-1]
#     conn.close()
#     return answer

def clear_dirtystr(str):
    return str.replace("'","")

def insert(_id, postNumber, lostDate, wechat,title,article,question,posterId,likes,postDate,isFound,status):
    conn = sqlite3.connect(db)
    sql = "INSERT INTO `lostFound`(`_id`, `postNumber`, `lostDate`, `wechat`,`title`,`article`,`question`,`posterId`,`likes`,`postDate`,`isFound`,`status`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');"
    c = conn.cursor()
    try:
        r = c.execute(sql.format(_id, postNumber, lostDate, wechat,title,article,question,posterId,likes,postDate,isFound,status))
    except sqlite3.IntegrityError as e: #dunplicate id
        # print e
        print '[!]dunplicate _id , data exists'
        print '[!]data has fresh! program exit...'
        sys.exit(-1)

    conn.commit()
    conn.close()


def update(question, answer_no):
    conn = sqlite3.connect(db)
    sql = "select `options` from `questions` where `quiz` = '{}'"
    c = conn.cursor()
    options = c.execute(sql.format(question)).fetchall()[-1][-1]
    answer = options.strip('[').strip(']').split()[answer_no - 1]
    sql = "UPDATE `questions` SET `answer`='{}' WHERE `quiz`='{}';"
    r = c.execute(sql.format(answer, question))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    for x in xrange(0,2500):
        req(x)
