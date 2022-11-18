from functools import partial

def resolve(el):
    if callable(el):
        return el()
    elif isinstance(el, (list,tuple)):
        return type(el)([resolve(x) for x in el])
    else:
        return el




class Lambda(object):
    def __init__(self,fun=None):
        self.fun = fun or (lambda x:x)
        
    def __getattr__(self,k):
        temp=lambda x:getattr(self(x), k)
        return self.__class__(temp)

    def __call__(self,x):
        return resolve(self.fun(x))
    
    def args(self,*_args,**kwargs):
        return self.__class__(lambda x:partial(self.fun(x),*_args,**kwargs))
    
    def __add__(self,other):
        return self.__class__(lambda x:self(x)+other)

    def length(self):
        return Lambda(lambda x:len(self(x)))


    def __ge__(self, other):
        return Lambda(lambda x:self(x)>=other)

    def __gt__(self, other):
        return Lambda(lambda x:self(x)>other)
    
    def __le__(self, other):
        return Lambda(lambda x:self(x)<=other)

    def __lt__(self, other):
        return Lambda(lambda x:self(x)<other)
    
    def __eq__(self,other):
        return Lambda(lambda x:self(x)==other)
    
    def __ne__(self, other):
        return Lambda(lambda x:self(x)!=other)
    
    def __getitem__(self,i):
        return  self.__class__(lambda x:self(x)[i])
    
    def __and__(self, other):
        return  self.__class__(lambda x:self(x) and other(x) )
        
    def __or__(self, other):
        
        return  self.__class__(lambda x:self(x) or other(x) )

    def isin(self,*elements):
        return Lambda(lambda x:self(x) in set(elements))
    
    def __contains__(self, el):
        return Lambda(lambda x:el in x)
    
class Not(Lambda):
    def __call__(self, x):
        return not Lambda.__call__(self, x)

class LambdaIterable(Lambda):
    def __getattr__(self,k):
        temp=lambda x:recgetattr(self(x), k)
        return self.__class__(temp)


        
    def __call__(self,x):
        if isinstance(x, (tuple,list,set)):
            return type(x)([self(y) for y in x])
        else:
            return resolve(self.fun(x))

def recgetattr(obj,k):
    if isinstance(obj, (tuple,list,set)):
        return type(obj)(recgetattr(x,k) for x in obj )
    else:
        return getattr(obj, k)
    
class Fun:
    def __init__(self,fun=None):
        self.fun = fun
    
    def __getattr__(self,k):
        return Fun(lambda x:globals()[k](self(x)))
    
    def __call__(self,x):    
        if self.fun:
            return self.fun(x)
        else:
            return x
        
if __name__=="__main__":
    x=Lambda()    
    c1=x>1
    c2=x<5
    print((c1&c2)(2))
    