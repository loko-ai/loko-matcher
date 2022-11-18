from ds4biz_matcher.business.matchers import RegexMatcher, NormMatcher

rm = RegexMatcher("andrea", flags=0)

om = NormMatcher(rm, lambda x: x.lower())

s = "Il sig Andrea Lenzi è andato questa mattina; presto a lavoro insieme alla signora Cecilia aledip06@yahoo.it"

for el in om.all(s.split()):
    print(el)
