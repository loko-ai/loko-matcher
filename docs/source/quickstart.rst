Quickstart
=========================

cond_matcher_example.py
------------------------------------
Example::

	from ds4biz_matcher.business.commons import is_iban
	from ds4biz_matcher.business.matchers import CondMatcher, MatchExpand
	
	cm = CondMatcher(is_iban)
	me = MatchExpand(cm,1,2)
	
	s = "Il sig Andrea Lenzi è andato questa mattina; presto a lavoro insieme alla signora Cecilia aledip06@yahoo.it IT 60X0542811101000000123456"
	
	for el in me.all(s.split()):
	    print(el)


extract_matches_example.py
------------------------------------
Example::

	from ds4biz_matcher.business.matchers import extract_matches, SynMatcher, RegexMatcher, Skipper
	
	rm = RegexMatcher(".+?@.+?\.(it|com)")
	start_m = SynMatcher({"Via","Viale","Piazza"})
	end_m = RegexMatcher("\d+")
	me = Skipper(start_m, end_m,max_skip=10)
	
	
	s = "Il sig Andrea Lenzi è andato questa mattina; Piazza del beato spirito dell'incoronata 19 presto a lavoro insieme alla signora Cecilia aledip06@yahoo.it IT 60X0542811101000000123456 In Via Salaria 719 succedono cose strane"
	
	for el in extract_matches(s.split(), ind=me, email=rm):
	    print(el)
	


fuzzy_matcher_example.py
------------------------------------
Example::

	from ds4biz_matcher.business.matchers import FuzzyMatcher, Multi
	
	fm = FuzzyMatcher("aledipyahoo", t=.5)
	
	s = "Il sig Andrea Lenzi è andato questa mattina; presto a lavoro insieme alla signora Cecilia aledip06@yahoo.it"
	
	for el in fm.all(s.split()):
	    print(el)
	
	
	fm = FuzzyMatcher("Andrei")
	fm2 = FuzzyMatcher("Lenz")
	
	mm = Multi(fm, fm2)
	
	s = "Il sig Andrea Lenzi è andato questa mattina; presto a lavoro insieme alla signora Cecilia aledip06@yahoo.it"
	
	for el in mm.all(s.split()):
	    print(el)
	


match_expand_example.py
------------------------------------
Example::

	from ds4biz_matcher.business.matchers import MatchExpand, RegexMatcher
	
	rm = RegexMatcher("Andrea")
	
	
	om = MatchExpand(rm,1,4)
	
	s = "Il sig An d rea Lenzi è andato questa mattina; presto a lavoro insieme alla signora Cecilia aledip06@yahoo.it"
	
	for el in om.all(s.split()):
	    print(el)


multi_matcher_example.py
------------------------------------
Example::

	from ds4biz_matcher.business.matchers import SynMatcher, Multi
	
	m = SynMatcher({"sig","sig.ra","signore","signora"})
	m2 = SynMatcher({"Andrea", "Cecilia"})
	mm = Multi(m, m2)
	
	
	
	s = "Il sig Andrea Lenzi è andato questa mattina presto a lavoro insieme alla signora Cecilia e alla sig.ra Camila"
	
	for el in mm.all(s.split()):
	
	    print(el)


norm_matcher_example.py
------------------------------------
Example::

	from ds4biz_matcher.business.matchers import RegexMatcher, NormMatcher
	
	rm = RegexMatcher("andrea", flags=0)
	
	om = NormMatcher(rm, lambda x: x.lower())
	
	s = "Il sig Andrea Lenzi è andato questa mattina; presto a lavoro insieme alla signora Cecilia aledip06@yahoo.it"
	
	for el in om.all(s.split()):
	    print(el)
	


or_matcher_example.py
------------------------------------
Example::

	from ds4biz_matcher.business.matchers import OrMatcher, FuzzyMatcher
	
	fm = FuzzyMatcher("Andrei")
	fm2 = FuzzyMatcher("Lenz")
	
	om = OrMatcher([fm,fm2])
	
	s = "Il sig Andrea Lenzi è andato questa mattina; presto a lavoro insieme alla signora Cecilia aledip06@yahoo.it"
	
	for el in om.all(s.split()):
	    print(el)


regex_matcher_example.py
------------------------------------
Example::

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


skipper_example.py
------------------------------------
Example::

	from ds4biz_matcher.business.matchers import Skipper, SynMatcher, RegexMatcher
	
	start_m = SynMatcher({"Via","Viale","Piazza"})
	end_m = RegexMatcher("\d+")
	me = Skipper(start_m, end_m,max_skip=10)
	
	s = "Il sig Andrea Lenzi è andato questa mattina; Piazza del beato spirito dell'incoronata 19 presto a lavoro insieme alla signora Cecilia aledip06@yahoo.it IT 60X0542811101000000123456 In Via Salaria 719 succedono cose strane"
	
	for el in me.all(s.split()):
	    print(el)


syn_matcher_example.py
------------------------------------
Example::

	from ds4biz_matcher.business.matchers import SynMatcher
	
	m = SynMatcher({"sig","sig.ra","signore","signora"})
	
	
	s = "Il sig Andrea Lenzi è andato questa mattina presto a lavoro insieme alla signora Cecilia"
	
	for el in m.all(s.split()):
	
	    print(el)


