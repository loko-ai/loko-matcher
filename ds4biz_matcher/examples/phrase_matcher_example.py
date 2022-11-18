from ds4biz_matcher.business.matchers import SpanMatcher, RegexMatcher

rm = RegexMatcher("Andrea")


om = SpanMatcher(rm,1,4)

s = "Il sig An d rea Lenzi è andato questa mattina; presto a lavoro insieme alla signora Cecilia aledip06@yahoo.it"

for el in om.all(s.split()):
    print(el)