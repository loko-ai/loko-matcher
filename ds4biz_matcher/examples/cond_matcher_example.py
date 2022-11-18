from ds4biz_matcher.business.commons import is_iban
from ds4biz_matcher.business.matchers import CondMatcher, SpanMatcher
from ds4biz_matcher.business.tokenizers import SimpleTokenizer

cm = CondMatcher(is_iban)
me = SpanMatcher(cm,1,2)

tokenizer = SimpleTokenizer()

s = "Il sig Andrea Lenzi è andato questa mattina; presto a lavoro insieme alla signora Cecilia aledip06@yahoo.it IT 60X0542811101000000123456"

for el in me.all(tokenizer.tokenize(s)):
    print(el)