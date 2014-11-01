#! /usr/bin/env python
#coding=utf-8
'''
模拟登陆新浪微博网页版
时间：2014.1.17
'''

import urllib
import urllib2
import cookielib
import re
import json
import base64
import rsa
import binascii
import random 
import requests

class WEIBO_LOGIN:
   
    
    def __init__(self):
        
        cj=cookielib.LWPCookieJar()
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        global headers
        headers = {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)','Referer':''}
    
    
    def getcanshu(self):
        # 获取参数（serverime，nonce，pubkey，）
        url='http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=cnNodWp1JTQwMTYzLmNvbQ%3D%3D&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.11)&_=1389944079340'
        req = urllib2.Request(url ,urllib.urlencode({}), headers)
        resp = urllib2.urlopen(req)
        login_page = resp.read()
        #print login_page
        p = re.compile('\((.*)\)')
        try:
            json_data = p.search(login_page).group(1)
            data = json.loads(json_data)
            servertime = str(data['servertime'])
            nonce = data['nonce']
            pubkey = str(data['pubkey'])
            rsakv = data['rsakv']
        
            return servertime, nonce, pubkey, rsakv
        except:
            print 'Get severtime error!'
            return None
        
        
    
    def jiami(self,username,password,servertime,nonce,pubkey):
        #加密用户名
        username = urllib.quote(username)
        usname = base64.encodestring(username)[:-1]
        
        #加密密码
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey,65537)
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
        passwd = rsa.encrypt(message,key)
        psd = binascii.b2a_hex(passwd)
        
        return usname, psd
    
    
    def loginweibo(self,usname, psd, servertime, nonce, rsakv):
        
        #模拟登陆
        url='http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)'
        data = urllib.urlencode({'entry':'weibo',
                                'gateway':'1',
                                'savestate':'7',
                                'useticket':'1',
                                'vsnf':'1',
                                'su':usname,
                                'service':'miniblog',
                                'servertime':servertime,
                                'nonce':nonce,
                                'pwencode':'rsa2',
                                'rsakv':rsakv,
                                'sp':psd,
                                'encoding':'UTF-8',
                                'prelt':'52',
                                'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
                                'returntype':'META'
                                })
        
        req  = urllib2.Request(url,data,headers)
        result = urllib2.urlopen(req)
        text = result.read()
        
        #获取返回值text里面的body中的url，并对此url使用GET方法来向服务器发请求，保存这次请求的Cookie信息
        p = re.compile('location\.replace\(\'(.*?)\'\)')
        try:
            login_url = p.search(text).group(1)
            urllib2.urlopen(login_url)
            print 'Login sussessed !'
        except:
            print 'Login error!'
     
    
    def denglu(self):
        #登陆web
        username = 'jbymsolo@sina.com'
        password = '5585bian'       
        servertime, nonce, pubkey, rsakv = self.getcanshu()
        usname, psd = self.jiami(username,password,servertime,nonce,pubkey)
        self.loginweibo(usname, psd, servertime, nonce, rsakv)
        
     
        
    def fetch(self,url):
        
        #不用代理ip
        
        result = urllib2.urlopen(url)
        text = result.read()
        return text
        
        #代理ip方法一
        '''
        suijishu=random.randrange(0, len(self.proxylist)-1)
        proxy= self.proxylist[suijishu]
        print proxy
        proxyes='http://'+proxy
        proxyes1={'http':proxyes}
        proxy_support = urllib2.ProxyHandler(proxyes1)
        opener=urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        
        
        result = urllib2.urlopen(url)
        text = result.read() 
        return text  
        '''
        #代理ip方法二
        '''
        opener1 = urllib.FancyURLopener(proxyes1)
        f = opener1.open(url)
        return f.read()
        '''