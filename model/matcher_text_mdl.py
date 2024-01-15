from typing import List


class Text4Matcher:
    def __init__(self, text: str = None, tokens: List[str] = None, rules: str = None):
        self.text = text
        self.rules = rules
        self.tokens = tokens
