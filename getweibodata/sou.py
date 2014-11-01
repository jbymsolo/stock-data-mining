#! /usr/bin/env python
#coding=utf-8
import urllib
import urllib2
import lxml.html as HTML
import re
import lxml.html.soupparser as soupparser
from wenjian import *
import mysql  
import sys
reload(sys)  
sys.setdefaultencoding('utf8') 

#读取一页的微博内容，并把它存入临时数据库（在存之前会把数据库中之前内容删除）
def ss(s,stockid):

    
     #连接数据库并删除之前内容
    conmysql = mysql.CON_MYSQL()
    shujuku = 'socNet'
    conmysql.selectdb(shujuku)
    sql = 'DELETE FROM %s' %('tmp'+str(stockid))
    conmysql.changesql(sql)
    conmysql.subm()
    text = s
    #用xpath解析出微博内容存在的脚本script
    dom = soupparser.fromstring(text)
    x = dom.xpath('./script[last()-7]/text()')
    
    #用正则表达式解析出所有微博的dl
        
    pdl = re.compile(r"<dl.*<\\\/dl>")
    try:
         
        mm= pdl.search(x[0]).group()
    except:
        yanzhengma =  '''!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!注意   注意   注意  注意!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!现在  你遇  到了  验证码 问题!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!所以  你必须   处理验证码!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!如何处理呢，非常简单!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!也就是你必须从网页登陆微博输入验证码!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!！
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ''' 
        print yanzhengma.decode('utf-8').encode('gb2312')
        
    
    #清洗微博内容把所有的\/转换成/
    pd2 = re.compile(r"\\\/")
    mm= pd2.sub('/',mm)
    
    #解析每个dl，取出微博内容
    dom = HTML.fromstring(mm)
    for i in range(1,21):

        #mid 在dl的属性里面，并解析出数字
        try:
            mid = dom.xpath('/html/div/dl['+str(i)+']/@mid')

            pd3 = re.compile(r"\d+")
            mid = pd3.search(mid[0]).group()
        except:
            break
        
        #微博昵称，微博发布时间，微博发布客户端在p的a里面
        try:
            uname = dom.xpath('/html/div/dl['+str(i)+']/dd/p/a[1]/text()')
            uname = uname[0].decode('raw_unicode_escape')
        except:
            uname = 'NA'

            
        try:
            time = dom.xpath('/html/div/dl['+str(i)+']/dd/p/a[1]/text()')
            time = time[1].decode('raw_unicode_escape')
        except:
            time ='NA'
            

        try:            
            here = dom.xpath('/html/div/dl['+str(i)+']/dd/p/a[2]/text()')
            here = here[0].decode('raw_unicode_escape')
        except:
            here = 'NA'

        
        #微博内容 在p的em里面
        content = dom.xpath('/html/div/dl['+str(i)+']/dd/p/em//text()')
        neirong = ''
        for con in content:
            neirong = neirong + con
        neirong = neirong.decode('raw_unicode_escape')
        
        #如果微博是转发，则微博的原博主和原内容，如果没用则为NA，NA
        yuanuname = ''
        yuanneirong = ''
        try:
            pd4 = re.compile(r"@")
            yuanuname = dom.xpath('/html/div/dl['+str(i)+']/dd/dl/dt/a/text()')
            yuanuname = pd4.sub('',yuanuname[0])
            yuanuname = yuanuname.decode('raw_unicode_escape')
            content1 = dom.xpath('/html/div/dl['+str(i)+']/dd/dl/dt/em//text()')
            for con in content1:
                yuanneirong = yuanneirong + con
            yuanneirong = yuanneirong.decode('raw_unicode_escape')
        except IndexError:
            yuanuname = 'NA'
            yuanneirong = 'NA'
        
        #赞的数量
        try:
            zan = dom.xpath('/html/div/dl['+str(i)+']/dd/p[2]/span/a[1]/text()')
            pd4 = re.compile(r"\d+")            
            zan = pd4.search(zan[0]).group()
        except IndexError:
            zan = 0
         
        #转发数量
        try:
            zhuanfa = dom.xpath('/html/div/dl['+str(i)+']/dd/p[2]/span/a[2]/text()')
            zhuanfa = zhuanfa[0].decode('raw_unicode_escape')            
            zhuanfa = pd4.search(zhuanfa).group()
        except :
            zhuanfa = 0
        
        #收藏数量
        try:
            shoucang = dom.xpath('/html/div/dl['+str(i)+']/dd/p[2]/span/a[3]/text()')
            shoucang = shoucang[0].decode('raw_unicode_escape')            
            shoucang = pd4.search(shoucang).group()
        except :
            shoucang = 0
            
        #评论数量
        try:
            pinglun = dom.xpath('/html/div/dl['+str(i)+']/dd/p[2]/span/a[3]/text()')
            pinglun = pinglun[0].decode('raw_unicode_escape')
            pinglun = pd4.search(pinglun).group()
        except :
            pinglun = 0
        
        
        sql = "insert into %s values('%s','%s','%s','%s','%s','%s','%s',%s,%s,%s,%s)" %('tmp'+str(stockid),mid,uname,neirong,yuanuname,yuanneirong,time,here,zan,zhuanfa,shoucang,pinglun)
        conmysql.changesql(sql)
        conmysql.subm()
        
   
#这一块是测试dt下边有哪些标签，标签是什么
'''
neirong1 = dom.xpath('/html/div/dl['+str(i)+']/dd/dl/dt/*')
for x in neirong1:
    print x.tag
print len(neirong1) 
'''
#微博中转码的方式
'''
x='\u53bblinkedin\u4e86 '
print x.decode('raw_unicode_escape')
print x.decode('utf-8')
print x.encode('utf-8')
'''
        
#微博中测试该数据的类型方式
'''
import chardet
chardet.detect(rawdata)  
'''
        
#beautifulsoup的使用方式        
'''
soup=BeautifulSoup(mm)
ss=soup.findAll('dl')
soup1=BeautifulSoup(str(ss))
s1=soup1.findAll('a')
'''    
