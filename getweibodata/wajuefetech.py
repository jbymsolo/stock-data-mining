#! /usr/bin/env python
#coding=utf-8
'''
获取信息

目的：获取微博内容搜索并存入数据库，只要目的是解决异常问题
时间：2014年5月9号
说明：这段代码还有一点漏洞：就是当连续两个股票上一次都有错误时，第二个会继承第一个错误的位置
但连续两个错误，或者开始读的时候，里面已经存留了上次没处理的错误。
所以，人为的解决方案就是每次读取的时候，不留下未读完的数据（而这段代码就是为这样设计的）。
'''
from sou import *
import urllib
import urllib2
import wajuelogin
import mysql
import lxml.html as HTML
import time
import lxml.html.soupparser as soupparser
import lxml.etree as etree
import sys 
import time
from threading import Thread


login = wajuelogin.WEIBO_LOGIN()
login.denglu()


def lianjieshujuku(stockid):
    
    global conmysql
    conmysql = mysql.CON_MYSQL()
    sql = 'CREATE DATABASE IF NOT EXISTS socNet'
    conmysql.createdb(sql)
    shujuku = 'socNet'
    conmysql.selectdb(shujuku)
    '''
    sql = CREATE TABLE IF NOT EXISTS weibo (mid BIGINT NOT NULL,uname CHAR(40),neirong TEXT,yuanuname CHAR(40),
            yuanneirong TEXT,time CHAR(20),here CHAR(20),zan INT(250),zhuanfa INT(250),shoucang INT(250),pinglun INT(250)) 
    conmysql.createdb(sql)
    '''
    sql = '''CREATE TABLE IF NOT EXISTS %s (mid BIGINT NOT NULL,uname CHAR(40),neirong TEXT,yuanuname CHAR(40),
            yuanneirong TEXT,time CHAR(20),here CHAR(20),zan INT(250),zhuanfa INT(250),shoucang INT(250),pinglun INT(250))''' %('tmp' + str(stockid))
    conmysql.createdb(sql)
    sql = 'CREATE TABLE IF NOT EXISTS %s (firmid BIGINT,lastmid BIGINT,nn BIGINT)' %('canzhao' + str(stockid))
    conmysql.createdb(sql)
    conmysql.subm()
      


#获取搜索内容
def sousuo(ss1,firmid,lastmid,nn,stockid,abc1):
    global abc
    abc = abc1
    returnmid = 0
    s1=urllib.quote(ss1)
    s222=urllib.quote(s1)      
    #读取新的数据
    if nn==0:
        print ('开始收集'+ss1+'的数据').decode('utf-8').encode('gb2312')
        for m in range(1,51): #过会改成51 
            abc = m+1
            time.sleep(0.1)
            zhongduancanshu = 0
            print ('正在读取股票：'+ss1+'的第' + str(m) + '页' ).decode('utf-8').encode('gb2312')
            ssurl2 = 'http://s.weibo.com/wb/'+str(s222)+'&xsort=time&nodup=1&page='+str(m)
            s = login.fetch(ssurl2)
            ss(s,stockid)          
            try:
                sql = "select * from %s" %('tmp'+str(stockid))
                result = conmysql.excutesql(sql)
                mid = result[0][0]
                #只把第一页的第一个mid返回去
                if m == 1:
                    returnmid = mid
                for i in range(0,len(result)):
                    lastmid = firmid
                    mid = result[i][0]
                    if mid <= firmid :
                        print '======================================='
                        nn = 0
                        print '更新微博结束'.decode('utf-8').encode('gb2312')
                        #删掉
                        sql = 'DELETE FROM %s' %('canzhao'+str(stockid))
                        conmysql.changesql(sql)
                        
                        sql = "insert into %s values('%s','%s','%s')" % (('canzhao'+str(stockid)),returnmid,lastmid,nn)
                        conmysql.changesql(sql)
                        conmysql.subm()
                        zhongduancanshu = 1
                        break
                    
                    else:
                        try:
                              
                            sql = "insert into west_weibo values('%s','%s','%s','%s','%s','%s','%s',%d,%d,%d,%d)" % (result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],result[i][5],result[i][6],result[i][7],result[i][8],result[i][9],result[i][10])
                            conmysql.changesql(sql)
                            conmysql.subm()
                            nn = mid
                            sql = 'DELETE FROM %s' %('canzhao'+str(stockid))
                            conmysql.changesql(sql)
                            sql = "insert into %s values('%s','%s','%s')" % (('canzhao'+str(stockid)),returnmid,lastmid,nn)
                            conmysql.changesql(sql)
                            conmysql.subm()
                        except:
                            print 'insert'+str(m)+' ye  and  the '+str(i)+' tiao  failed, this pages  have '+str(len(result))+' weibo,you must processing again!!!!!!!'
                            #删掉

                            sql = 'DELETE FROM %s' %('canzhao'+str(stockid))
                            conmysql.changesql(sql)

                            
                            sql = "insert into %s values('%s','%s','%s')" % (('canzhao'+str(stockid)),returnmid,lastmid,nn)
                            conmysql.changesql(sql)
                            conmysql.subm()  
                            
                
                    
                    if m >= 50:
                        nn = 0
                        print '*********************************************'
                        print '这是第一次读取，第一次读取50页结束'.decode('utf-8').encode('gb2312')
                        #删掉
                        sql = 'DELETE FROM %s' %('canzhao'+str(stockid))
                        conmysql.changesql(sql)
                        
                        sql = "insert into %s values('%s','%s','%s')" % (('canzhao'+str(stockid)),returnmid,lastmid,nn)
                        conmysql.changesql(sql)
                        conmysql.subm()
                        break
            except:
                print '读取临时微博出错，tmp中可能没有东西，所以这一页略过'.decode('utf-8').encode('gb2312')
            if zhongduancanshu ==1:
                break
            
            
           
        
                                    
    #紧接着处理上次有错误的读取，是为了上次更完整。
    else:
        print '接着处理上次读取失败'.decode('utf-8').encode('gb2312')
        for m in range(abc,51): #过会改成51
            abc = abc + 1
            print ('正在处理上次失败的地方股票：'+ss1+'的第' + str(m) + '页' ).decode('utf-8').encode('gb2312')
            zhongduancanshu1 = 0
            time.sleep(0.1)
            ssurl2 = 'http://s.weibo.com/wb/'+str(s222)+'&xsort=time&nodup=1&page='+str(m)
            s = login.fetch(ssurl2)                    
            ss(s,stockid)
            try:
                sql = "select * from %s" %('tmp'+str(stockid))
                result = conmysql.excutesql(sql)

                returnmid = firmid
                for i in range(0,len(result)):
                    mid = result[i][0]
                    if mid > lastmid and mid < nn:
                        try:                        
                            sql = "insert into west_weibo values('%s','%s','%s','%s','%s','%s','%s',%d,%d,%d,%d)" % (result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],result[i][5],result[i][6],result[i][7],result[i][8],result[i][9],result[i][10])
                            conmysql.changesql(sql)
                            conmysql.subm()
                            nn = mid
                            
                            sql = 'DELETE FROM %s' %('canzhao'+str(stockid))
                            conmysql.changesql(sql)
                                                    
                            sql = "insert into %s values('%s','%s','%s')" % ('canzhao'+str(stockid),returnmid,lastmid,nn)                        
                            conmysql.changesql(sql)
                            conmysql.subm()

                        except:
                            print '修改又失败了，你必须重新启动程序'.decode('utf-8').encode('gb2312')
                            #删掉
                            sql = 'DELETE FROM %s' %('canzhao'+str(stockid))
                            conmysql.changesql(sql)
                            
                            sql = "insert into %s values('%s','%s','%s')" % ('canzhao'+str(stockid),returnmid,lastmid,nn)
                            conmysql.changesql(sql)
                            conmysql.subm()
                            break
                        
                    elif mid <= lastmid:
                        
                        nn = 0
                        print '恭喜你，修改成功'.decode('utf-8').encode('gb2312')
                        print '++++++++++++++++++++++++++++++++++++++'
                        #删掉____
                        sql = 'DELETE FROM %s' %('canzhao'+str(stockid))
                        conmysql.changesql(sql)

                        sql = "insert into %s values('%s','%s','%s')" % (('canzhao'+str(stockid)),returnmid,lastmid,nn)
                        conmysql.changesql(sql)
                        conmysql.subm()
                        zhongduancanshu1 = 1
                        break
                                        

            except:
                print '读取临时微博出错，tmp中可能没有东西，所以这一页略过'.decode('utf-8').encode('gb2312')
            if m >= 50:
                nn = 0
                print '恭喜，修改成功,并且可能你好久没有读取微博数据了'.decode('utf-8').encode('gb2312')
                print '++++++++++++++++++++++++++++++++++++++'
                #删掉____
                sql = 'DELETE FROM %s' %('canzhao'+str(stockid))
                conmysql.changesql(sql)
                                    
                sql = "insert into %s values('%s','%s','%s')" % (('canzhao'+str(stockid)),returnmid,lastmid,nn)
                conmysql.changesql(sql)
                conmysql.subm()
                zhongduancanshu1 = 1
                break
            
            
            if zhongduancanshu1 ==1:
                break
            


stock = {   1:"太极股份", 
            2:"苏宁云商",
            3:"兴业银行",
            4:"民生银行",
            5:"贵州茅台", 
            6:"三泰电子", 
            7:"歌尔声学", 
            8:"白云山", 
            9:"乐视网", 
            10:"中国平安", 
            11:"北特科技", 
            12:"富邦股份", 
            13:"一心堂", 
            14:"今世缘", 
            15:"龙大肉食", 
            16:"飞天诚信", 
            17:"浦发银行", 
            18:"山水文化", 
            19:"新南洋", 
            20:"浦发银行",
            21:"招商银行" 
            }
def run(stockid,abc1):
    lianjieshujuku(stockid)
    try:
        sqlbianliang = 'select * from %s' %('canzhao' + str(stockid))
        kongzhibianliang = conmysql.excutesql(sqlbianliang)
    except:
        print '从数据库中读取 firmid，lastmid失败'.decode('utf-8').encode('gb2312')
    
    try:          
        firmid = kongzhibianliang[0][0]
        lastmid = kongzhibianliang[0][1]
        nn = kongzhibianliang[0][2]                
    except:
        firmid = 0
        lastmid = 0
        nn = 0 
    sousuo(stock[stockid],firmid,lastmid,nn,stockid,abc1)
    conmysql.closeconn
       

    '''
        note:
        当第一个有异常时，设置xm = 当前出错的数字，
        你必须去微博，输入验证码，然后继续。
        停留30之后继续读。        
    '''
if __name__=='__main__':
    
    try:
        for stockid in stock:
            
            s = ' 正在读第 ' + str(stockid) +' 个股票: '+stock[stockid]
            print s.decode('utf-8').encode('gb2312')
            xm= stockid
            run(stockid,1)
    except:
        abcd = abc -1
        try:
            time.sleep(20)
            for m in range(xm,22):
                if m > xm:
                    abcd = 1
                s = ' 正在读第 ' + str(m) + ' 个股票: '+stock[m]
                print s.decode('utf-8').encode('gb2312')
                xm1 = m
                run(m,abcd)
        except:
            abcd = abc -1    
            try:
                time.sleep(20)
                for m in range(xm1,22):
                    if m > xm1:
                        abcd = 1
                    s = ' 正在读第 ' + str(m) + ' 个股票: '+stock[m]
                    print s.decode('utf-8').encode('gb2312')
                    xm1 = m                      
                    run(m,abcd)
            except:
                abcd = abc -1
                try:
                    time.sleep(20)
                    for m in range(xm1,22):
                        if m > xm1:
                            abcd = 1
                        s = ' 正在读第 ' + str(m) + ' 个股票: '+stock[m]
                        print s.decode('utf-8').encode('gb2312')
                        xm1 = m
                        run(m,abcd)
                except:
                    abcd = abc -1
                    try:
                        time.sleep(20)
                        for m in range(xm1,22):
                            if m > xm1:
                                abcd = 1                            
                            s = ' 正在读第 ' + str(m) + ' 个股票: '+stock[m]
                            print s.decode('utf-8').encode('gb2312')
                            xm1 = m
                            run(m,abcd)
                    except:
                        abcd = abc -1
                        time.sleep(20)
                        for m1 in range(xm1,22):
                            if m > xm1:
                                abcd = 1
                            s = ' 正在读第 ' + str(m1) + ' 个股票: '+stock[m1]
                            print s.decode('utf-8').encode('gb2312')
                            xm1 = m
                            run(m,abcd)
    finally:
        if xm1 >= 21:
            print '''
            !!!!!!!!!!!!!!!!!
            所有weibo运行结束
            !!!!!!!!!!!!!!!!!'''.decode('utf-8').encode('gb2312')
        else:
            print '''
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            很遗憾，更新微博没有结束，你必须重新启动
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''.decode('utf-8').encode('gb2312')
                            
                            
                