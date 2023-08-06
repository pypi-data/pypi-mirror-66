from .. import colors
from .tokenizer import AccessLogTokenizer


class AccessLogColorFormatter:
    """ rebuild message with colors depending on the http code """

    def __init__(self, log_format):
        self._tokenizer = AccessLogTokenizer(log_format)

    def format(self, record):
        log_parts = self._tokenizer.match_dict(record.msg)
        http_code = int(log_parts["s"])
        color_str = colors.BRIGHT
        if http_code >= 500:
            color_str = colors.RED
        elif http_code >= 400:
            color_str = colors.YELLOW
        if color_str:
            for field in ["r", "s"]:
                log_parts[field] = f"{color_str}{log_parts[field]}{colors.RESET}"
        msg = self._tokenizer.rebuild()
        record.msg = msg
        return msg
