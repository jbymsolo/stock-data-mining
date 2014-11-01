#encoding=utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.core.context_processors import csrf
from west.models import sousuo
from west.models import weibo
import sys
import time
daytime = time.strftime("%Y-%m-%d %H:%M:%S")

reload(sys)   
sys.setdefaultencoding('utf8')  



def jieguo(request):
    

    if request.POST:
        sousou  = request.POST['soso']
        new_record = sousuo(sstime = daytime,ssneirong = sousou)
        new_record.save()
      
      
    ctx ={}
    ctx.update(csrf(request))

    mylist = weibo.objects.filter(uname=sousou)
   
    #ctx['rlt'] = mylist
    #staff_str  = map(str, mylist)
    
    #staff_str  = [e.uname, for e in mylist]
    try :
        for e in mylist:
            pass

    #return HttpResponse("<p>" + x + "</p>")
    #return render(request,'jieguo.html', {'names':  mylist})
        return render(request, "form.html", {'names':  mylist})
    except :
        pass
    
    '''
    db = MySQLdb.connect(user='root', db='socNet', passwd='jbymsolo', host='localhost')
    cursor = db.cursor()
    cursor.execute('SELECT uname,neirong FROM weibo')

    uames = [row[0] for row in cursor.fetchall()]
    neirong = [row[1] for row in cursor.fetchall()]   
    db.close()
    #return render_to_response('jieguo.html', {'names': uames})
    #return render(request,'jieguo.html', {'names': uames})
    return HttpResponse("<p>%s</p>" %uames)
    '''

  
        
    
