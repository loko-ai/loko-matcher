from ds4biz_matcher.business.matchers import OrMatcher, FuzzyMatcher

fm = FuzzyMatcher("Andrei")
fm2 = FuzzyMatcher("Lenz")

om = OrMatcher(fm,fm2)

s = "Il sig Andrea Lenzi è andato questa mattina; presto a lavoro insieme alla signora Cecilia aledip06@yahoo.it"

for el in om.all(s.split()):
    print(el)