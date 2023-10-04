from enum import Enum


class TokenType(Enum):
    SYMBOL = 1
    KEYWORD = 2
    ALPHA = 3
    NUM = 4
    COMMENT = 5
    NONE = 99


class State(Enum):
    IDENTIFIER = 1
    SYMBOL = 2
    KEYWORD = 3
    COMMENT = 4
    NUMERIC = 5
    ALPHANUMERIC = 6
    INEXISTENT = 99


class Token:
    classe: TokenType
    valor: str

    def __init__(self, valor: str, classe: TokenType) -> None:
        self.valor = valor
        self.classe = classe

    def __str__(self) -> str:
        return f"Token({self.classe}, {self.valor})"


# fmt: off
SYMBOLS_LIST = [
    "(", ")",
    "{", "}",
    "[", "]",
    "/", "/*", "*/",
    "+", "-", "*",
    "=", "==",
    "<", "<=",
    ">", "=>",
    "!", "!=",
    ",", ";"
]
# fmt: on

KEYWORDS_LIST = [
    "if",
    "else",
    "while",
    "int",
    "return",
    "void",
]
