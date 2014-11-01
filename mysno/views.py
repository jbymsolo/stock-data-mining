#encoding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
from weibo import APIClient

APP_KEY = '15531345' # app key
APP_SECRET = '91ceb992d9a8e7c8d10aa595d63c7fa6' # app secret
CALLBACK_URL = 'http://www.example.com/callback' # callback url



def first_page(request):
    return render(request, 'first.html')


