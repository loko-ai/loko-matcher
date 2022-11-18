from ds4biz_matcher.business.matchers import SynMatcher, Multi

m = SynMatcher({"sig","sig.ra","signore","signora"})
m2 = SynMatcher({"Andrea", "Cecilia"})
mm = Multi(m, m2)



s = "Il sig Andrea Lenzi è andato questa mattina presto a lavoro insieme alla signora Cecilia e alla sig.ra Camila"

for el in mm.all(s.split()):

    print(el)