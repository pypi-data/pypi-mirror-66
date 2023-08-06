import re
from enclosed import Parser, TokenType


class AccessLogTokenizer:

    part_regex = {
        "h": r"(?P<h>\S+)",  # host %h
        "l": r"(?P<l>\S+)",  # indent %l (unused)
        "u": r"(?P<u>\S+)",  # user %u
        "t": r"(?P<t>\[.+\])",  # time %t
        "r": r"(?P<r>.*)",  # request "%r"
        "s": r"(?P<s>[0-9]+)",  # status %>s
        "b": r"(?P<b>\S+)",  # size %b (careful, can be '-')
        "f": r"(?P<f>.*)",  # referrer "%{Referer}i"
        "a": r"(?P<a>.*)",  # user agent "%{User-agent}i"
    }

    def __init__(self, log_format):
        parser = Parser()
        tokens = parser.tokenize(log_format)
        msg_regex = ""
        for token_type, token_pos, token_text in tokens:
            if token_type is TokenType.ENCLOSED:
                token_regex = self.part_regex[token_text]
            else:
                token_regex = token_text
            msg_regex += token_regex

        self._tokens = tokens
        self.log_pattern = re.compile(msg_regex)

    def match_dict(self, msg):
        self._log_parts = self.log_pattern.match(msg).groupdict()
        return self._log_parts

    def rebuild(self):
        msg = ""
        for token_type, token_pos, token_text in self._tokens:
            if token_type is TokenType.ENCLOSED:
                msg_part = self._log_parts[token_text]
            else:
                msg_part = token_text
            msg += msg_part
        return msg
