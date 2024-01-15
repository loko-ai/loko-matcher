import json
from typing import Dict

from ds4biz_matcher.business.matchers import PhraseMatcher, Skipper, RegexMatcher, OrMatcher, FuzzyMatcher
from ds4biz_matcher.business.tokenizers import MatchPreservingTokenizer, SimpleTokenizer
from ds4biz_matcher.model.matches import Match
from ds4biz_matcher.business import parser
from loguru import logger

from model.matcher_text_mdl import Text4Matcher
from utils.matcher_utils import jsonify_matches, get_matcher_request_fmt

example_txt = "La sig.ra Maria e il sig. Giovanni Storti vanno al mare e versano € 700 sul conto LT 60X 0542811101000000123456"

#todo Verificare "span" matcher con "lower" e anche "phrase" matcher con il "post"  (in questo caso applica il post-processing solo al primo token matchato, e perde gli altri)

example = Text4Matcher(example_txt, rules='regex("La")')

numbers = Skipper(RegexMatcher("\d+"), RegexMatcher("\d+"), 10, skipcond=RegexMatcher("[\d+\-\._/]"))

points = PhraseMatcher(OrMatcher(FuzzyMatcher("num"), "n"), ".")

st = MatchPreservingTokenizer(SimpleTokenizer(sep="\\s+", puncts=".,;:!?\"'()"), PhraseMatcher("sig", ".", "ra"),
                              numbers, points)

def extract_txt_matches(text: Text4Matcher = example,  include_tokens: bool=True) -> Dict[str, dict]: #include_matches_location: bool=True,
    logger.debug("starting matches extraction from text")
    if text.tokens is None:
        logger.debug("tokenizing the text")
        tokens = st.tokenize(text.text)
    else:
        logger.debug("text already tokenized")
        tokens = text.tokens
    matchers_return = dict()
    indices = set()
    matches_info = []
    matches_text = []
    logger.debug("collecting all the matches")
    for m in parser.get_matcher(text.rules).all(tokens):
        matches_text.append(m.tokens)
        json_match = jsonify_matches(m)
        matches_info.append(json_match)
        indices.update(list(range(m.start, m.end)))
    logger.debug(f"matches found {len(matches_text)}")
    matchers_return["matches_text"] = matches_text
    matchers_return["matches"] = matches_info
    if include_tokens:
        tokens_info = []
        for token_idx, token in enumerate(tokens):
            if token_idx in indices:
                tokens_info.append((token, True))
            else:
                tokens_info.append((token, False))
        matchers_return["tokens"]= tokens_info
    return matchers_return

