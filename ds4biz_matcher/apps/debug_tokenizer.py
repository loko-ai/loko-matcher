from ds4biz_matcher.business.matchers import Skipper, RegexMatcher,\
    PhraseMatcher
from ds4biz_matcher.business.tokenizers import SimpleTokenizer,\
    MatchPreservingTokenizer
from ds4biz_matcher.business.matchers import SpanMatcher
numbers= SpanMatcher(RegexMatcher("\\d+[\.,\-/\d]+\\d+"),1,40)


simple=SimpleTokenizer(SimpleTokenizer(sep="\\s+",puncts=".,;:!?\"'()"))

mail=RegexMatcher("\w+.+?\w+@.+")
st=MatchPreservingTokenizer(SimpleTokenizer(sep="\\s+",puncts=".,;:!?\"'()"),PhraseMatcher("sig",".","ra"), numbers,mail)


text="il numero ID amics@sdsadsa.it 10-23.20.50,30 / 75 /  222 e invece il 101.340 per il sig . ra Fulvio"

print(st.tokenize(text))
for el in numbers.all(simple.tokenize(text)):
    print(el.tokens)