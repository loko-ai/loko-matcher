import json
from typing import List, Union

from model.matcher_text_mdl import Text4Matcher


def get_matcher_request_fmt(text: Union[str, List[str]]=None, rules: str=None):
    if isinstance(text, list):
        return Text4Matcher(tokens=text, rules=rules)
    elif isinstance(text, str):
        return Text4Matcher(text=text, rules=rules)
    else:
        raise Exception(f"The input value's format ({type(text)}) is not supported. Provide a string or a list of string to match your rules.")


def jsonify_matches(match):
    return json.loads(
        json.dumps(match, default=lambda obj: getattr(obj, '__dict__', str(obj)))
    )