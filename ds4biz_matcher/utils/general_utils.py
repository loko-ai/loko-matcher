def flatten(s):
    if isinstance(s, (list,tuple)):
        ret=[]
        for x in s:
            ret.extend(flatten(x))
        return ret
    else:
        return [s]
    
