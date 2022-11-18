import re
class RE:
    def __init__(self,regex,terminate="$"):
        self.regex = regex
        self.terminate = terminate
        
    def __add__(self,other):
        return RE(self.regex+other.regex)
    
    def __call__(self,text,flags=0):
        return re.match(self.regex+self.terminate, text, flags=flags)

    def rep(self,_min=0,_max=None):
        if _min==0 and _max==None:
            mod="*?"
        elif _min==1 and max==None:
            mod="+"
        else:
            mod="{%d,%d}"%(_min,_max)
        return RE("%s%s"%(self.regex,mod))
    
    def search(self,text,flags=0):
        return re.findall(self.regex,text,flags)
    
    
    
temp=RE("a").rep(2,3)+RE("b")

print(temp.regex)
print(temp.search("aab"))