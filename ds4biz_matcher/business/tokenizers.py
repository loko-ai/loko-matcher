import re
import string
from ds4biz_matcher.business.matchers import OrMatcher
import spacy


class SimpleTokenizer:
    def __init__(self,puncts=string.punctuation,sep=" +"):
        self.puncts = puncts
        self.sep = sep
        self.exceptions=set()
        
    def __call__(self,text):
        
        for el in re.split(self.sep,text):
            if el in self.exceptions:
                yield el
            else:
                el=re.sub("([%s])"%self.puncts," \\1 ",el)
                for t in re.split(" +",el):
                    if t:
                        yield t
                        
    def tokenize(self,text):
        return list(self(text))
    
class MatchPreservingTokenizer:
    def __init__(self,tokenizer,*matchers):
        self.matchers = OrMatcher(*matchers)
        self.tokenizer = tokenizer
        
    def __call__(self,text):
        tokens=self.tokenizer.tokenize(text)
        i=0
        while i<len(tokens):
            match=self.matchers.match_at(i,tokens)
            if match:
                yield "".join(match.tokens)
                i+=len(match)
            else:
                yield tokens[i]
                i+=1
                
    def tokenize(self,text):
        return list(self(text))


class SpacyTokenizer:
    def __init__(self,language):
        self.language = language
        self.nlp = spacy.load(language)
        
    def tokenize(self,text:str):
        doc=self.nlp(text)
        return [token for token in doc]

                    
            
        
