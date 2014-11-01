#-*- coding: utf8 -*-

'''
时间：2014,5,8
目的：连接数据库，创建数据库，创建表格，选择数据库，增删改查
'''
import MySQLdb

class CON_MYSQL:
    
    #构造函数，连接数据库
    def __init__(self):
        try:
            global conn,cur
            conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='jbymsolo',port=3306,charset="utf8")
            cur=conn.cursor()
        except MySQLdb.Error,e:
             print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    #创建数据库或者表       
    def createdb(self,sql):
        try:
            cur.execute(sql)
        except MySQLdb.Error,e:
             print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    #选择数据表    
    def selectdb(self,shujuku):
        try:
            conn.select_db(shujuku)
        except MySQLdb.Error,e:
             print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
    #增改
    def changesql(self,sql):
        try:
            cur.execute(sql)
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    
             
    #查
    def excutesql(self,sql):
        try:
            cur.execute(sql)
            result = cur.fetchall()
            return result
        except MySQLdb.Error,e:
             print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
    #提交
    def subm(self):
        try:
            conn.commit()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        
        

    #关闭数据库
    def closeconn(self):
        try:
            cur.close()
            conn.close()
        except MySQLdb.Error,e:
             print "Mysql Error %d: %s" % (e.args[0], e.args[1])

 





