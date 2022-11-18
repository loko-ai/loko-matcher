from ds4biz_matcher.business.matchers import RegexMatcher

rm = RegexMatcher(".+?@.+?\.(it|com)")


s = "Il sig Andrea Lenzi è andato questa mattina; presto a lavoro insieme alla signora Cecilia aledip06@yahoo.it"

for el in rm.all(s.split()):

    print(el)


rm = RegexMatcher("mattina",junk=";")

for el in rm.all(s.split()):

    print(el)


rm = RegexMatcher("a",terminate="$")


for el in rm.all(s.split()):

    print(el)