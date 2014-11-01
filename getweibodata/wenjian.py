

def openwenjian(x,y):
    global f1
    f1=open(x,y)


def xiewenjian(x):
    f1.write(x)


def closewenjian():
    f1.close()
