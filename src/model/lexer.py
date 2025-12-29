from typing import List, Set, Optional, Tuple
from .token import Token, TokenType

class LexicalAnalyzer:
    """
    A professional-grade lexical analyzer for a C-like language.
    
    Attributes:
        source_code (str): The code to analyze.
        tokens (List[Token]): The list of generated tokens.
        errors (List[str]): A list of error messages encountered during analysis.
    """

    # Static definitions for language grammar
    KEYWORDS: Set[str] = {
        'if', 'else', 'while', 'for', 'do', 'switch', 'case',
        'default', 'break', 'continue', 'return', 'goto',
        'int', 'float', 'double', 'char', 'void', 'short',
        'long', 'signed', 'unsigned', 'const', 'volatile',
        'static', 'extern', 'auto', 'register', 'struct',
        'union', 'enum', 'typedef', 'sizeof',
        'bool', 'true', 'false', 'input', 'printf', 'scanf'
    }

    OPERATORS: Set[str] = {
        '+', '-', '*', '/', '=', '<', '>', '!', '&', '|', '%', '^', '~', '?', '#'
    }

    DELIMITERS: Set[str] = {
        '(', ')', '{', '}', '[', ']', ';', ',', ':', '.'
    }

    COMBINED_OPS: Set[str] = {
        '==', '!=', '<=', '>=', '&&', '||', '+=', '-=', '*=', '/=', 
        '++', '--', '->', '%=', '<<', '>>', '&=', '^=', '|=', '~=', 
        '<<=', '>>='
    }

    def __init__(self):
        self.source_code: str = ""
        self.tokens: List[Token] = []
        self.errors: List[str] = []
        self._token_counter: int = 1

    def analyze(self, source_code: str) -> List[Token]:
        """
        Performs lexical analysis on the given source code.
        
        Args:
            source_code (str): The raw source code to tokenize.
            
        Returns:
            List[Token]: A list of Token objects found in the code.
        """
        self.source_code = source_code
        self.tokens = []
        self.errors = []
        self._token_counter = 1
        
        # Pre-process: Remove comments (simple approach, could be integrated into main loop for better sourcemapping)
        # Note: In a true professional compiler, we might keep comments as trivia or handle them in the main loop
        # to preserve exact line numbers for everything. Here, we follow the original logic but refactored.
        cleaned_code, comment_errors = self._remove_comments_keeping_structure(source_code)
        self.errors.extend(comment_errors)
        
        self._tokenize_code(cleaned_code)
        return self.tokens

    def _remove_comments_keeping_structure(self, source: str) -> Tuple[str, List[str]]:
        """
        Removes comments but replaces them with whitespace to preserve line/column numbering 
        for subsequent tokens.
        """
        result: List[str] = list(source)
        errors: List[str] = []
        i = 0
        n = len(source)
        
        while i < n:
            # Check for strings to avoid clearing comments inside strings
            if result[i] in '"\'':
                quote = result[i]
                i += 1
                while i < n:
                    if result[i] == '\\' and i + 1 < n: # Escape
                        i += 2
                        continue
                    if result[i] == quote:
                        i += 1
                        break
                    i += 1
                continue

            # Line comment //
            if i + 1 < n and source[i] == '/' and source[i+1] == '/':
                # Replace everything until newline with space
                result[i] = ' '
                result[i+1] = ' '
                i += 2
                while i < n and result[i] != '\n':
                    result[i] = ' '
                    i += 1
                continue

            # Block comment /* */
            if i + 1 < n and source[i] == '/' and source[i+1] == '*':
                start_line = source.count('\n', 0, i) + 1
                start_col = i - source.rfind('\n', 0, i)
                
                result[i] = ' '
                result[i+1] = ' '
                i += 2
                closed = False
                while i < n:
                    if i + 1 < n and result[i] == '*' and result[i+1] == '/':
                        result[i] = ' '
                        result[i+1] = ' '
                        i += 2
                        closed = True
                        break
                    
                    if result[i] != '\n': # Keep newlines to preserve line numbers
                        result[i] = ' '
                    i += 1
                
                if not closed:
                    errors.append(f"Unclosed block comment starting at Line {start_line}, Column {start_col}")
                continue

            i += 1
            
        return "".join(result), errors

    def _tokenize_code(self, code: str) -> None:
        """Internal method to scan the code and produce tokens."""
        i = 0
        n = len(code)
        curr_line = 1
        curr_col = 1
        
        # Helper to track position
        def advance(amount=1):
            nonlocal i, curr_col
            i += amount
            curr_col += amount

        while i < n:
            char = code[i]
            
            # 1. Handle Whitespace
            if char in ' \t\r':
                # Special tab handling for column accuracy if needed, here simple
                if char == '\t':
                    curr_col += 3 # Assume tab is 4 spaces, we added 1 already by loop logic if we didn't differentiate
                advance()
                continue
            
            if char == '\n':
                i += 1
                curr_line += 1
                curr_col = 1
                continue
            
            # 2. Strings
            if char == '"':
                start_line = curr_line
                start_col = curr_col
                
                string_val = ""
                # Don't add the opening quote to value if we want just content, 
                # but standard lexers often include it or just content. 
                # Original included quotes, let's include quotes.
                string_val += char
                advance() 
                
                closed = False
                while i < n:
                    c = code[i]
                    if c == '\\' and i + 1 < n: # Escape
                        string_val += c + code[i+1]
                        advance(2)
                        continue
                    if c == '"':
                        string_val += c
                        advance()
                        closed = True
                        break
                    if c == '\n':
                        curr_line += 1
                        curr_col = 1 # Reset col but keep i moving
                        i += 1
                        # We don't advance curr_col strictly for newline char in this simplified loop
                        # but we need to track it manually if we are inside string
                        string_val += c
                        continue
                        
                    string_val += c
                    advance()
                
                if not closed:
                    self.errors.append(f"Line {start_line}, Column {start_col}: Unclosed string literal")
                    self._add_token(TokenType.UNCLOSED_STRING, string_val + "...", start_line, start_col)
                else:
                    self._add_token(TokenType.STRING, string_val, start_line, start_col)
                continue

            # 3. Numbers
            if char.isdigit():
                start_line = curr_line
                start_col = curr_col
                num_str = ""
                dot_count = 0
                
                while i < n and (code[i].isdigit() or code[i] == '.'):
                    if code[i] == '.':
                        dot_count += 1
                    num_str += code[i]
                    advance()
                
                if dot_count > 1 or num_str.endswith('.'):
                    self.errors.append(f"Line {start_line}, Column {start_col}: Invalid number format '{num_str}'")
                    self._add_token(TokenType.INVALID, num_str, start_line, start_col)
                else:
                    self._add_token(TokenType.NUMBER, num_str, start_line, start_col)
                continue

            # 4. Identifiers & Keywords
            if char.isalpha() or char == '_':
                start_line = curr_line
                start_col = curr_col
                ident_str = ""
                
                while i < n and (code[i].isalnum() or code[i] == '_'):
                    ident_str += code[i]
                    advance()
                
                if ident_str in self.KEYWORDS:
                    self._add_token(TokenType.KEYWORD, ident_str, start_line, start_col)
                else:
                    self._add_token(TokenType.IDENTIFIER, ident_str, start_line, start_col)
                continue
                
            # 5. Operators (Multi and Single)
            if char in self.OPERATORS:
                start_line = curr_line
                start_col = curr_col
                op_str = char
                
                # Check next char for combined
                if i + 1 < n:
                    combined = char + code[i+1]
                    if combined in self.COMBINED_OPS:
                        # Check for 3-char ops (like <<=)
                        if i + 2 < n:
                            combined_3 = combined + code[i+2]
                            if combined_3 in self.COMBINED_OPS:
                                op_str = combined_3
                                advance(3)
                                self._add_token(TokenType.OPERATOR, op_str, start_line, start_col)
                                continue
                        
                        op_str = combined
                        advance(2)
                        self._add_token(TokenType.OPERATOR, op_str, start_line, start_col)
                        continue
                
                # If not combined
                advance()
                self._add_token(TokenType.OPERATOR, op_str, start_line, start_col)
                continue

            # 6. Delimiters
            if char in self.DELIMITERS:
                self._add_token(TokenType.DELIMITER, char, curr_line, curr_col)
                advance()
                continue
            
            # 7. Invalid/Unknown
            self.errors.append(f"Line {curr_line}, Column {curr_col}: Invalid character '{char}'")
            self._add_token(TokenType.INVALID, char, curr_line, curr_col)
            advance()

    def _add_token(self, type: TokenType, value: str, line: int, col: int):
        self.tokens.append(Token(type, value, line, col, self._token_counter))
        self._token_counter += 1
