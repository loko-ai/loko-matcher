import re
from typing import Set, List
from difflib import SequenceMatcher
from _collections import defaultdict
from ds4biz_matcher.utils.textutils import rangegram, rangegram_at
from abc import abstractmethod
from ds4biz_matcher.model.matches import Match
import itertools
from ds4biz_matcher.utils.match_utils import match_picker, longest_match, \
    shortest_match, best_match
from collections import Counter
from ds4biz_matcher.utils.general_utils import flatten


class Matcher:
    """The base class for every matcher"""

    def all(self, tokens: List[str]):
        """Returns an iterator over matches in the given tokenized sequence"""
        i = 0
        while i < len(tokens):
            temp = self.match_at(i, tokens)
            if temp:
                yield temp
                i += len(temp)
            else:
                i += 1

    @abstractmethod
    def __call__(self, token: str):
        pass

    def match_at(self, i: int, tokens: List[str]):
        if i < len(tokens):
            score = self(tokens[i])
            if score:
                return Match(i, tokens[i], score)
            else:
                return None
        else:
            return None

    def has_match(self, tokens, n: int = 1):
        return len(list(self.all(tokens))) >= n


class MatchAll(Matcher):
    def __call__(self, token: str):
        return 1.0


class SimpleMatcher(Matcher):

    def __init__(self, value: str):
        self.value = value

    def __call__(self, token):
        if str(token) == self.value:
            return 1.0
        else:
            return 0


def ensure_matchers(matchers):
    return [ensure_matcher(m) for m in matchers]


def ensure_matcher(matcher):
    if isinstance(matcher, str):
        return SimpleMatcher(matcher)
    elif isinstance(matcher, Matcher):
        return matcher

    elif callable(matcher):
        return CondMatcher(matcher)

    raise Exception("Can't ensure matcher")


class SynMatcher(Matcher):
    """Returns a match if a token is in the set of options ex: {Mister,Mr.,Signore}"""

    def __init__(self, options: Set):
        self.options = options

    def __call__(self, token):
        if str(token) in self.options:
            return 1.0
        else:
            return 0


def consecutive(i, tokens, *matchers):
    submatches = []
    for m in matchers:
        match = m.match_at(i, tokens)
        if match:
            submatches.append(match)
            i += len(match.tokens)
        else:
            return None
    if submatches:
        return Match.from_submatches(submatches)
    else:
        return None


class PhraseMatcher(Matcher):
    """Returns a match if all the sub-matchers have adjacent matches"""

    def __init__(self, *matchers):
        self.matchers = ensure_matchers(matchers)

    @abstractmethod
    def __call__(self, token: List[str]):
        return consecutive(0, token)

    def match_at(self, i: int, tokens: List[str]):
        return consecutive(i, tokens, *self.matchers)


class RegexMatcher(Matcher):
    """A regexp based matcher
    """

    def __init__(self, regex, flags=re.IGNORECASE, junk="", terminate="$"):  # @UndefinedVariable
        self.regex = regex
        self.flags = flags
        self.junk = junk
        self.terminate = terminate

    def __call__(self, token):
        token = str(token)
        token = "".join([x for x in token if x not in self.junk])
        if re.match(self.regex + self.terminate, token, self.flags):
            return 1.0
        else:
            return 0


class FuzzyMatcher(Matcher):
    """A fuzzy matcher with a given threshold t"""

    def __init__(self, ent, t=.8):
        self.ent = ent
        self.t = t

    def __call__(self, token):
        token = str(token)
        if self.ent == token:
            return 1.0
        s = SequenceMatcher(None, self.ent, token)
        score = s.ratio()
        if callable(self.t):
            tt = self.t(token)
        else:
            tt = self.t
        if score >= tt:
            return score
        else:
            return 0


class OrMatcher(Matcher):
    """Returns a match if any of the submatchers does"""

    def __init__(self, *matchers):
        self.matchers = ensure_matchers(matchers)

    def __call__(self, token):
        return max([m(token) for m in self.matchers])

    def match_at(self, i: int, tokens: List[str]):
        matches = []
        for m in self.matchers:
            match = m.match_at(i, tokens)
            if match:
                matches.append(match)
        if matches:
            return best_match(matches)
        else:
            return None

    def all(self, tokens: List[str]):
        for m in self.matchers:
            yield from m.all(tokens)


class SpanMatcher(Matcher):
    """"""

    def __init__(self, matcher, m, n, separator="", strategy="longest"):
        self.m = m
        self.n = n
        self.matcher = ensure_matcher(matcher)
        self.separator = separator
        self.strategy = strategy

    def match_at(self, i, tokens):
        matches = []
        for el in rangegram_at(i, tokens, self.m, self.n):
            score = self(el)
            if score:
                matches.append(Match(i, el, score))
        if not matches:
            return None
        if callable(self.strategy):
            return match_picker(matches, self.strategy)
        else:
            if self.strategy == "longest":
                return longest_match(matches)
            elif self.strategy == "shortest":
                return shortest_match(matches)
            elif self.strategy == "best":
                return best_match(matches)
            else:
                raise Exception("Strategy %s not supported" % self.strategy)

    def __call__(self, token):
        if self.separator != None:
            return self.matcher(self.separator.join([str(x) for x in token]))
        else:
            return self.matcher(token)


class NormMatcher(Matcher):
    def __init__(self, matcher, fun):
        self.matcher = ensure_matcher(matcher)
        self.fun = fun

    def __call__(self, token):
        if isinstance(token, (list, tuple)):
            token = (self.fun(x) for x in token)
        else:
            token = self.fun(token)
        return self.matcher(token)

    def match_at(self, i: int, tokens: List[str]):
        match = self.matcher.match_at(i, [self.fun(x) for x in tokens])
        if match:
            match.tokens = tokens[match.start:match.start + len(match)]
        return match


class Lower(NormMatcher):
    def __init__(self, matcher):
        super().__init__(matcher, lambda x: str(x).lower())


class CondMatcher(Matcher):
    """A matcher based on an user-defined condition (one-argument callable)"""

    def __init__(self, cond):
        self.cond = cond

    def __call__(self, token):
        if self.cond(token):
            return 1.0
        else:
            return 0


def fsm(submatches, tokens):
    start_match = min(submatches, key=lambda x: x.start)
    end_match = max(submatches, key=lambda x: x.start + len(x))
    start = start_match.start
    end = end_match.start + len(end_match)

    ntokens = tokens[start:end]
    score = sum([x.score for x in submatches])

    return Match(start, ntokens, score, submatches=submatches)


class ContextMatcher(Matcher):
    def __init__(self, *matchers, max_dist=100):
        self.matchers = ensure_matchers(matchers)
        self.max_dist = max_dist

    def all(self, tokens: List[str]):
        matches = {}
        for m in self.matchers:
            for match in m.all(tokens):
                matches[match.start] = match

        temp = []
        start = 0
        for i in sorted(matches.keys()):
            match = matches[i]
            if start and abs(i - start) > self.max_dist:
                if temp:
                    yield fsm(temp, tokens)
                    temp = [match]
            else:
                temp.append(match)
            start = match.start
        if temp:
            yield fsm(temp, tokens)


class Skipper(Matcher):
    def __init__(self, start_matcher, end_matcher, max_skip=5, skipcond=MatchAll()):
        self.start_matcher = ensure_matcher(start_matcher)
        self.end_matcher = ensure_matcher(end_matcher)
        self.max_skip = max_skip
        self.skipcond = ensure_matcher(skipcond)

    def __call__(self, token):
        score1 = self.start_matcher(token[0])
        score2 = self.end_matcher(token[-1])
        if score1 and score2:
            return (score1 + score2) / 2
        else:
            return 0

    def match_at(self, i: int, tokens: List[str]):
        submatches = []
        m = self.start_matcher.match_at(i, tokens)
        if m:
            submatches.append(m)
            j = i + len(m)
            while len(submatches) < self.max_skip + 1:
                m2 = self.end_matcher.match_at(j, tokens)
                if m2:
                    return Match.from_submatches(submatches + [m2])

                else:
                    sub = self.skipcond.match_at(j, tokens)
                    if not sub:
                        return None
                    else:
                        submatches.append(sub)
                        j += len(sub)
            return None
        else:
            return None


class Repeating(Matcher):
    def __init__(self, matcher, minlen=1, maxlen=100):
        self.matcher = ensure_matcher(matcher)
        self.minlen = minlen
        self.maxlen = maxlen

    def __call__(self, token: str):
        return self.matcher(token)

    def match_at(self, i: int, tokens: List[str]):
        matches = []
        j = i
        while j < len(tokens):
            m = self.matcher.match_at(j, tokens)
            if m:
                matches.append(m)
                j += len(m)
            else:
                break
            if len(matches) >= self.maxlen:
                break
        if len(matches) >= self.minlen:
            return Match.from_submatches(matches)
        else:
            return None


class PermMatcher(Matcher):
    def __init__(self, *matchers):
        self.matchers = ensure_matchers(matchers)

    def match_at(self, i: int, tokens: List[str]):
        matches = []
        for x in itertools.permutations(self.matchers):
            match = PhraseMatcher(*x).match_at(i, tokens)
            if match:
                matches.append(match)
        if matches:
            return best_match(matches)
        else:
            return None


class Expand(Matcher):
    def __init__(self, matcher, left=10, right=10):
        self.matcher = ensure_matcher(matcher)
        self.left = left
        self.right = right

    def __call__(self, token: str):
        return self.matcher.match(token)

    def match_at(self, i: int, tokens: List[str]):
        match = self.matcher.match_at(self.left + i, tokens)
        if match:
            start = max(0, match.start - self.left)
            end = min(len(tokens), match.end + self.right)
            return Match(i, tokens[start:end], match.score, [match])
        else:
            return None

    def all(self, tokens: List[str]):
        for match in self.matcher.all(tokens):
            start = max(0, match.start - self.left)
            end = min(len(tokens), match.end + self.right)
            yield Match(start, tokens[start:end], match.score, [match])


class ChainMatcher(Matcher):
    def __init__(self, matcher1, matcher2):
        self.matcher1 = ensure_matcher(matcher1)
        self.matcher2 = ensure_matcher(matcher2)

    def match_at(self, i: int, tokens: List[str]):
        raise Exception("Not supported")

    def all(self, tokens):
        for m in self.matcher1.all(tokens):
            for m2 in self.matcher2.all(m.tokens):
                yield Match(m.start + m2.start, m2.tokens, score=m2.score)


class FilterMatcher(Matcher):
    def __init__(self, matcher, cond):
        self.matcher = ensure_matcher(matcher)
        self.cond = cond

    def __call__(self, token: str):
        return self.matcher(token) and self.cond(token)

    def match_at(self, i: int, tokens: List[str]):
        match = self.matcher.match_at(i, tokens)
        if match and self.cond(match, len(tokens)):
            return match
        else:
            return None

    def all(self, tokens: List[str]):
        for m in self.matcher.all(tokens):
            if self.cond(m, len(tokens)):
                yield m


class ExpandFilterMatcher(Matcher):
    def __init__(self, matcher, cond, left=10, right=10):
        self.matcher = ensure_matcher(matcher)
        self.cond = cond
        self.left = left
        self.right = right

    def __call__(self, token: str):
        return self.matcher(token) and self.cond(token)

    def match_at(self, i: int, tokens: List[str]):
        match = self.matcher.match_at(i, tokens)
        if match:
            start = max(0, match.start - self.left)
            end = min(len(tokens), match.end + self.right)
            if self.cond(Match(i, tokens[start:end], match.score, [match]), len(tokens)):
                return match

        return None

    def all(self, tokens: List[str]):
        for match in self.matcher.all(tokens):
            start = max(0, match.start - self.left)
            end = min(len(tokens), match.end + self.right)
            if self.cond(Match(start, tokens[start:end], match.score, [match]), len(tokens)):
                yield match


def overlaps(start_1, end_1, start_2, end_2):
    return start_1 <= start_2 < end_1 or start_2 <= start_1 < end_2


def overlappings(matches):
    while matches:
        m = matches.pop()
        keep = True
        for m2 in list(matches):
            if overlaps(m.start, m.end, m2.start, m2.end):
                # print("Over",m.start,m.end,m2.start,m.end)
                if m2.score > m.score:
                    keep = False
                    break
                else:
                    # print("Removing",m2)
                    matches.remove(m2)
        if keep:
            yield m


class Exclude(Matcher):
    def __init__(self, matcher):
        self.matcher = ensure_matcher(matcher)

    def __call__(self, token: str):
        return self.matcher(token)

    def _purge(self, m):
        if m:
            m.tokens = ["" for x in m.tokens]
        return m

    def match_at(self, i: int, tokens: List[str]):
        match = self.matcher.match_at(i, tokens)
        if match:

            return self._purge(match)
        else:
            return None


class PostProcess(Matcher):
    def __init__(self, matcher, f):
        self.matcher = matcher
        self.f = f

    def __call__(self, token: str):
        return self.matcher(token)

    def _process(self, m):
        if m:
            m.tokens = self.f(m.tokens)
        return m

    def match_at(self, i: int, tokens: List[str]):
        match = self.matcher.match_at(i, tokens)
        if match:

            return self._process(match)
        else:
            return None

    def all(self, tokens: List[str]):
        for m in self.matcher.all(tokens):
            yield self._process(m)


class SpacyMatcher(Matcher):
    def __init__(self, entities=None):
        self.entities = entities

    def match_at(self, i: int, tokens: List[str]):
        raise Exception("Not implemented")

    def all(self, tokens: List[str]):
        if tokens:
            for ent in tokens[0].doc.ents:
                if self.entities is None or ent.label_ in self.entities:
                    yield Match(ent.start, tokens[ent.start:ent.end], 1.0)


def extract_matches(tokens, **matchers):
    for k, m in matchers.items():
        for el in m.all(tokens):
            yield k, el


class Sub(Matcher):
    def __init__(self, matcher):
        self.matcher = ensure_matcher(matcher)

    def all(self, tokens: List[str]):
        ends = {}
        for m in self.matcher.all(tokens):
            if m.end in ends:
                if len(m) > m.end:
                    ends[m.end] = m
            else:
                ends[m.end] = m

        yield from ends.values()


class BackoffMatcher(Matcher):
    def __init__(self, *matchers):
        self.matchers = ensure_matchers(matchers)

    def match_at(self, i: int, tokens: List[str]):
        for m in self.matchers:
            ret = m.match_at(i, tokens)
            if ret:
                return ret
        return None

    def all(self, tokens: List[str]):
        for m in self.matchers:
            matches = list(m.all(tokens))
            if matches:
                yield from matches
                return

        yield from []


if __name__ == '__main__':
    matcher = RegexMatcher("12345")

    print(list(matcher.all(tokens=["ciao", "12345"])))
