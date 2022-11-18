from ds4biz_commons.utils.cache import FSCache
from typing import List, Dict
from pymongo.mongo_client import MongoClient
from ds4biz_matcher.business.matchers import RegexMatcher, Skipper,\
    PhraseMatcher, extract_matches, FuzzyMatcher, SpanMatcher, BestScore, Lower,\
    OrMatcher
from ds4biz_matcher.business.tokenizers import MatchPreservingTokenizer,\
    SimpleTokenizer
import itertools
from ds4biz_commons.utils.function_utils import shuffled
from bson.objectid import ObjectId
from tqdm._tqdm import tqdm


client=MongoClient('104.248.46.44', 27017)
db= client.aea


numbers= Skipper(RegexMatcher("\d+"),RegexMatcher("\d+"),10,skipcond=RegexMatcher("[\d+\-\./]"))

st=MatchPreservingTokenizer(SimpleTokenizer(sep="\\s+",puncts=".,;:!?\"'()_"),PhraseMatcher("sig",".","ra"), numbers)


class MongoDAO:
    def __init__(self,db,host=None,port=None):
        self.host = host
        self.port = port
        self.client=MongoClient(host,port)
        self.db = self.client[db]
        
    def list(self,collection):
        return list(self.db[collection].find())
    
    def save(self,collection,obj:Dict):
        if "id" in obj:
            obj["_id"]=obj.pop("id")
            
        if "_id" in obj:
            obj["_id"]=ObjectId(obj["_id"])
        
        return self.db[collection].save(obj)

    
    def find_one(self,collection,id):
        temp=self.db[collection].find_one({"_id":ObjectId(id)})
        print(temp,collection)
        return temp
    
    def delete(self,collection,_id):
        return self.db[collection].remove(dict(_id=ObjectId(_id)))

dao=MongoDAO("rules", '104.248.46.44', 27017)


@FSCache()
def get_documents()->List:
    temp=list(db.aea_docs_norm.find({},{"_id":0}))
    anns={v['id']:v for v in db.aea_annotations.find()}
        
    return [dict(__klass__="multidoc",content=dict(**x,annotations=anns.get(x['id'],{}))) for x in temp]


for doc in tqdm(itertools.islice(shuffled(get_documents()),0,100)):
    cont=doc['content']
    entities=cont['annotations']
    body=cont['id']+"\n"+cont['oggetto']+"\n"+"\n".join(cont['body_parts'])
    print(cont['id'])
    
    tokens=st.tokenize(body)
    for kk in {"_id","id","label"}:
        try:
            entities.pop(kk)
        except:
            pass
    docs=[("Body",body)]+[(k,v) for (k,v) in cont['attachments'].items()]
    
    for k,v in entities.items():
        if v:
            for ent in v:
                print("\t",k,ent)
                fm=Lower(FuzzyMatcher(ent.lower(),lambda x: .7 if len(x)>15 else .9 ))
                base=OrMatcher(SpanMatcher(fm,1,6),SpanMatcher(fm,1,8," "))
                for name,d in docs:
                    tokens=st.tokenize(d)
                    mm=list(BestScore(base).all(tokens))
                    for m in mm:
                        print("\t\t",name,m.tokens,m.start,m.score)
                    
                    
    
            
            
            