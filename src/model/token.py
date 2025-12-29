from enum import Enum, auto
from dataclasses import dataclass
from typing import Any

class TokenType(Enum):
    """
    Enumeration of all possible token types in the language.
    """
    KEYWORD = "Keyword"
    IDENTIFIER = "Identifier"
    NUMBER = "Number"
    OPERATOR = "Operator"
    DELIMITER = "Delimiter"
    STRING = "String"
    
    # Error types
    INVALID = "Invalid"
    UNCLOSED_STRING = "Unclosed String"
    UNCLOSED_COMMENT = "Unclosed Comment"

@dataclass(frozen=True)
class Token:
    """
    Immutable representation of a lexical token.
    
    Attributes:
        type (TokenType): The category of the token.
        value (str): The actual text content of the token.
        line (int): The line number where the token starts (1-based).
        column (int): The column number where the token starts (1-based).
        index (int): The sequential index of the token in the stream (1-based).
    """
    type: TokenType
    value: str
    line: int
    column: int
    index: int

    def __str__(self) -> str:
        return f"Token({self.type.value}, '{self.value}', Line:{self.line})"
