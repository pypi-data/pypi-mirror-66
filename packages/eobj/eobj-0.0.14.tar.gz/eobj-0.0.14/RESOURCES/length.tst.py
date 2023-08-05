class tst(object):
    def __init__(self):
        self.__dict__['x'] = 1000
    def f(self):
        print("function")
        pass
    def __getattribute__(self,an):
       print(an)
       return(object.__getattribute__(self,an))

