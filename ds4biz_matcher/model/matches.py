from ds4biz_matcher.utils.general_utils import flatten
from typing import List
class Match:
    def __init__(self,start:int,tokens:List[str],score:float,submatches:List=None):
        self.start = start
        self.score = score
        self.tokens = flatten(tokens)
        self.end = self.start+len(self.tokens)
        self.submatches=submatches
        
    @staticmethod
    def from_submatches(submatches):
        tokens=flatten([x.tokens for x in submatches])
        score= sum([x.score for x in submatches])/len(submatches)
        i=min([x.start for x in submatches])
        return Match(i,tokens,score,submatches)

    def __str__(self):
        return "Match "+str(self.__dict__)
    
    def __repr__(self):
        return "Match "+str(self.__dict__)
    
    def __len__(self):
        return len(self.tokens)
    
    def to_string(self,sep=" "):
        temp=[str(x) for x in self.tokens if x]
        return sep.join(temp)
        