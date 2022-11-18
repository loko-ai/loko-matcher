from ds4biz_matcher.business.matchers import SynMatcher

m = SynMatcher({"sig","sig.ra","signore","signora"})


s = "Il sig Andrea Lenzi è andato questa mattina presto a lavoro insieme alla signora Cecilia"

for el in m.all(s.split()):

    print(el.start,el.tokens)