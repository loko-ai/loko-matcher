from ds4biz_matcher.business.matchers import extract_matches, SimpleMatcher,\
    RegexMatcher
from collections import Counter
from ds4biz_matcher.business import parser
from ds4biz_matcher.business.tokenizers import SimpleTokenizer


def mc(counter):
    m=counter[max(counter,key=counter.get)]
    temp=counter.most_common()
    return [x[0] for x in temp if x[1]==m]

class RuleClassifier:
    def __init__(self,tokenizer,chooser=lambda x:x.most_common(len(x))[0][0]):
        self.chooser = chooser
        self.tokenizer = tokenizer
        self.rules={}
    
    def fit(self,X,y,**kwargs):
        return self
    
    def partial_fit(self,X,y,**kwargs):
        return self
    def add_rule(self,klass,rule):
        self.rules[klass]=rule
        
    def predict(self,X):
        for x in X:
            c=Counter()
            tokens=self.tokenizer.tokenize(x)
            for k,el in extract_matches(tokens,**self.rules):
                c[k]+=1 
                
        return self.chooser(c)
    
    
    
if __name__=="__main__":
    rc=RuleClassifier(SimpleTokenizer(),mc)
    rc.add_rule("SINISTRO", SimpleMatcher("sinistro"))
    rc.add_rule("PRATICA", SimpleMatcher("pratica"))
    rc.add_rule("GEN", RegexMatcher("quest.*"))
    
    print(rc.predict(["questo quest  è il mio sinistro e è la mia pratica pratica no sinistro"]))
    
    