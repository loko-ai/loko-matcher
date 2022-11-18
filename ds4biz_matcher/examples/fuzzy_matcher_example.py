from ds4biz_matcher.business.matchers import FuzzyMatcher, PhraseMatcher

fm = FuzzyMatcher("aledipyahoo", t=.5)

s = "Il sig Andrea Lenzi è andato questa mattina; presto a lavoro insieme alla signora Cecilia aledip06@yahoo.it"

for el in fm.all(s.split()):
    print(el)


fm = FuzzyMatcher("Andrei")
fm2 = FuzzyMatcher("Lenz")

mm = PhraseMatcher(fm, fm2)

s = "Il sig Andrea Lenzi è andato questa mattina; presto a lavoro insieme alla signora Cecilia aledip06@yahoo.it"

for el in mm.all(s.split()):
    print(el)
