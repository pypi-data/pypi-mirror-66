import threading

class MyThread(threading):
    '''
    使用继承的方法实现多线程，传递要处理的队列、所要使用的函数名即可
    '''
    def __init__(self):
        super().__init__()
    
    def run()