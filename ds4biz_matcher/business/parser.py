import schwifty
from ds4biz_matcher.business.matchers import ensure_matcher, SynMatcher, SimpleMatcher, Exclude, PostProcess, Expand, \
    ChainMatcher, \
    ContextMatcher, BackoffMatcher, Sub, ExpandFilterMatcher

from ds4biz_matcher.business.matchers import Lower, MatchAll, OrMatcher,\
    PhraseMatcher, RegexMatcher, Skipper, SpanMatcher, CondMatcher, FuzzyMatcher,\
    NormMatcher, PermMatcher, Repeating, FilterMatcher
import re
from ds4biz_matcher.utils.lambdas import Lambda, Not
from ds4biz_matcher.business.tokenizers import SimpleTokenizer
from ds4biz_matcher.business.commons import is_alphanumeric
from ds4biz_matcher.utils.interpreter import eval_last
import pkg_resources



def is_alphanumeric(s,minnum=1,minalpha=0):
    nums,alphas=0,0
    for ch in s:
        if ch.isdigit():
            nums+=1
        if ch.isalpha():
            alphas+=1
    return nums>=minnum and alphas>=minalpha

def is_iban(s):
    try:
        schwifty.IBAN(s)
        return True
    except:
        return False

def load(package,resource_name):
    return [x.strip() for x in set(open(pkg_resources.resource_filename(package,resource_name)).read().split("\n")) if x.strip()]


glob=dict(oneof=OrMatcher,regex=RegexMatcher,span=SpanMatcher,phrase=PhraseMatcher,lower=Lower,skip=Skipper,all=MatchAll(),
      condition=CondMatcher, rep=Repeating,fuzzy=FuzzyMatcher,perm=PermMatcher,norm=NormMatcher,token=Lambda(),
      filter=FilterMatcher,NOT=Not,re=re,is_alp=is_alphanumeric,syn=SynMatcher,load=load,is_iban=is_iban,
            simple=SimpleMatcher,exclude=Exclude,post=PostProcess,expand=Expand, expandfilter=ExpandFilterMatcher,
          chain=ChainMatcher,context=ContextMatcher,
          backoff=BackoffMatcher, sub=Sub)


def get_matcher(text:str):
    return ensure_matcher(eval_last(text,glob))
