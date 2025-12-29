class Theme:
    """
    Defines the color palette and constants for the professional UI.
    Using a 'Dracula'-inspired dark theme or a clean corporate slate theme.
    Let's go with a modern 'Slate' Business Theme.
    """
    
    # Colors
    PRIMARY = "#3b82f6"       # Bright Blue
    PRIMARY_HOVER = "#2563eb" # Darker Blue
    SECONDARY = "#64748b"     # Slate Grey
    
    BG_MAIN = "#f0f2f5"       # Very Light Grey (App Background)
    BG_PANEL = "#ffffff"      # White (Panels)
    BG_INPUT = "#f8fafc"      # Lightest Slate
    
    TEXT_MAIN = "#1e293b"     # Dark Slate (Main text)
    TEXT_DIM = "#64748b"      # Muted text
    TEXT_WHITE = "#ffffff"
    
    BORDER = "#e2e8f0"        # Light Border
    
    # Highlight Colors for Tokens
    TOKEN_KEYWORD = "#7c3aed"    # Violet
    TOKEN_IDENTIFIER = "#0f172a" # Dark Slate
    TOKEN_NUMBER = "#059669"     # Emerald Green
    TOKEN_STRING = "#ea580c"     # Orange
    TOKEN_OPERATOR = "#0891b2"   # Cyan
    TOKEN_DELIMITER = "#64748b"  # Slate
    TOKEN_ERROR = "#dc2626"      # Red
    
    # Fonts
    FONT_MAIN = ("Segoe UI", 10)
    FONT_BOLD = ("Segoe UI", 10, "bold")
    FONT_HEADER = ("Segoe UI", 12, "bold")
    FONT_CODE = ("Consolas", 10)
    
    # Dimensions
    PADDING_SMALL = 5
    PADDING_MEDIUM = 10
    PADDING_LARGE = 15
