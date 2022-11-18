from ds4biz_matcher.utils.jsonutils import GenericJsonEncoder
from flask import request, jsonify, Flask
from loko_extensions.business.decorators import extract_value_args

import json
from typing import List, Dict
from _collections import defaultdict
from ds4biz_matcher.model.matches import Match
from ds4biz_matcher.business import parser
from ds4biz_matcher.business.tokenizers import SimpleTokenizer, \
    MatchPreservingTokenizer
from ds4biz_matcher.business.matchers import PhraseMatcher, RegexMatcher, FuzzyMatcher, OrMatcher, Skipper

app = Flask("matcher")  # , static_folder=find_file("static"), static_url_path="/web")

example = "La sig.ra Maria e il sig. Giovanni Storti vanno al mare e versano € 700 sul conto IT 60X 0542811101000000123456"


class Text:
    def __init__(self, text: str = example, tokens: List[str] = None, rule: str = None):
        self.text = text
        self.rule = rule
        self.tokens = tokens


numbers = Skipper(RegexMatcher("\d+"), RegexMatcher("\d+"), 10, skipcond=RegexMatcher("[\d+\-\._/]"))

points = PhraseMatcher(OrMatcher(FuzzyMatcher("num"), "n"), ".")

st = MatchPreservingTokenizer(SimpleTokenizer(sep="\\s+", puncts=".,;:!?\"'()"), PhraseMatcher("sig", ".", "ra"),
                              numbers, points)


@app.post("/loko_extract")
@extract_value_args(_request=request)
def loko_extract(value, args):
    text = Text(**value)
    if text.tokens is None:
        tokens = st.tokenize(text.text)
    else:
        tokens = text.tokens
    print(tokens)
    indices = set()
    ret = []
    for m in parser.get_matcher(text.rule).all(tokens):
        ret.append(m)
        indices.update(list(range(m.start, m.end)))

    ii = []
    for i, el in enumerate(tokens):
        if i in indices:
            ii.append((el, True))
        else:
            ii.append((el, False))
    include_tokens = args.get("include_tokens")
    if include_tokens:

        return jsonify(dict(tokens=ii, matches=ret))
    else:
        return jsonify(ret)


# app.register_error_handler(Exception, basic_error_handler)
app.json_encoder = GenericJsonEncoder
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True)
