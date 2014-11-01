import os
import sys  
#Calculate the path based on the location of the WSGI script.  
apache_configuration= os.path.dirname(__file__)  
project = os.path.dirname(apache_configuration)  
workspace = os.path.dirname(project)  


os.chdir('D:/mysno/mysno')  
sys.stdout = sys.stderr   
sys.path.append(workspace)  
  
#print workspace   
sys.path.append(workspace + "mysno")  
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysno.settings'  
import django.core.handlers.wsgi  
application = django.core.handlers.wsgi.WSGIHandler() 