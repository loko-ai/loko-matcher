from ds4biz_matcher.business.matchers import extract_matches, SynMatcher, RegexMatcher, Skipper

rm = RegexMatcher(".+?@.+?\.(it|com)")
start_m = SynMatcher({"Via","Viale","Piazza"})
end_m = RegexMatcher("\d+")
me = Skipper(start_m, end_m,max_skip=10)


s = "Il sig Andrea Lenzi è andato questa mattina; Piazza del beato spirito dell'incoronata 19 presto a lavoro insieme alla signora Cecilia aledip06@yahoo.it IT 60X0542811101000000123456 In Via Salaria 719 succedono cose strane"

for el in extract_matches(s.split(), ind=me, email=rm):
    print(el[1].tokens)
