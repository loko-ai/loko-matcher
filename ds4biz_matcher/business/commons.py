import schwifty
import re


from ds4biz_matcher.business.matchers import FuzzyMatcher, OrMatcher,\
    RegexMatcher, CondMatcher

def is_alphanumeric(s,minnum=1,minalpha=0):
    nums,alphas=0,0
    for ch in s:
        if ch.isdigit():
            nums+=1
        if ch.isalpha():
            alphas+=1
    return nums>=minnum and alphas>=minalpha    


def orfuzzy(values,t=.8):
    return OrMatcher([FuzzyMatcher(x,t=t) for x in values])

def orregex(values,flags=re.IGNORECASE):  # @UndefinedVariable
    return OrMatcher([RegexMatcher(x,flags=flags) for x in values])


def is_iban(s):
    try:
        schwifty.IBAN(s)
        return True
    except:
        return False

def num_letters(n):
    return CondMatcher(lambda x:len(x)==n)


def is_upper_or_capitalized(s):
    return len(s)>1 and s[0].isupper()

