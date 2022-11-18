def ngram(l,n):
    for i in range(len(l)-n+1):
        yield tuple(l[i:i+n])

def rangegram(l,m,n):
    for i in range(m,n+1):
        
        yield from ngram(l,i)

def rangegram_at(i,l,m,n):
    for j in range(m,n+1):
        if i+j<=len(l):
            yield l[i:i+j]


