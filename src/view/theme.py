import tkinter as tk
from tkinter import ttk

class Theme:
    """
    Defines the color palette and constants for the professional UI.
    Implements a coherent design system for the application.
    """
    
    # --- Color Palette (Slate & Blue) ---
    PRIMARY         = "#2563eb"       # Vibrant Blue
    PRIMARY_HOVER   = "#1d4ed8"       # Darker Blue
    PRIMARY_FG      = "#ffffff"       # White text on primary
    
    BG_MAIN         = "#f1f5f9"       # Light Slate (App Background)
    BG_PANEL        = "#ffffff"       # White (Card/Panel Background)
    BG_INPUT        = "#f8fafc"       # Very Light Slate (Input/Editor)
    
    TEXT_MAIN       = "#0f172a"       # Dark Slate (Main text)
    TEXT_SECONDARY  = "#64748b"       # Muted Slate (Labels/Secondary)
    TEXT_DIM        = "#94a3b8"       # Dim text (Disabled/Placeholder)
    
    BORDER_LIGHT    = "#e2e8f0"       # Light Border
    BORDER_FOCUS    = "#3b82f6"       # Focused Border
    
    # --- Syntax Highlighting ---
    TOKEN_KEYWORD    = "#7c3aed"      # Violet
    TOKEN_IDENTIFIER = "#334155"      # Slate
    TOKEN_NUMBER     = "#059669"      # Emerald
    TOKEN_STRING     = "#ea580c"      # Orange
    TOKEN_OPERATOR   = "#0891b2"      # Cyan
    TOKEN_COMMENT    = "#94a3b8"      # Light Slate
    TOKEN_ERROR      = "#dc2626"      # Red
    
    # --- Typography ---
    FONT_FAMILY      = "Segoe UI"
    FONT_CODE_FAMILY = "Consolas"
    
    FONT_MAIN        = (FONT_FAMILY, 10)
    FONT_BOLD        = (FONT_FAMILY, 10, "bold")
    FONT_HEADER      = (FONT_FAMILY, 14, "bold")
    FONT_CODE        = (FONT_CODE_FAMILY, 11)
    
    @staticmethod
    def configure_style(root):
        """
        Configures the ttk.Style for the application.
        """
        style = ttk.Style(root)
        style.theme_use('clam')  # 'clam' provides a good base for customization
        
        # General Defaults
        style.configure(".", 
                        background=Theme.BG_MAIN, 
                        foreground=Theme.TEXT_MAIN, 
                        font=Theme.FONT_MAIN,
                        borderwidth=0)
        
        # --- Frames ---
        style.configure("Card.TFrame", background=Theme.BG_PANEL)
        style.configure("Main.TFrame", background=Theme.BG_MAIN)
        
        # --- Buttons ---
        # Primary Button
        style.configure("Primary.TButton",
                        background=Theme.PRIMARY,
                        foreground=Theme.PRIMARY_FG,
                        borderwidth=0,
                        focuscolor=Theme.PRIMARY,
                        padding=(15, 8),
                        font=Theme.FONT_BOLD)
        style.map("Primary.TButton",
                  background=[('active', Theme.PRIMARY_HOVER), ('pressed', Theme.PRIMARY_HOVER)],
                  foreground=[('active', Theme.PRIMARY_FG)])
        
        # Secondary/Default Button
        style.configure("TButton",
                        background=Theme.BG_PANEL,
                        foreground=Theme.TEXT_MAIN,
                        borderwidth=1,
                        bordercolor=Theme.BORDER_LIGHT,
                        lightcolor=Theme.BG_PANEL,
                        darkcolor=Theme.BG_PANEL,
                        padding=(15, 8),
                        font=Theme.FONT_MAIN)
        style.map("TButton",
                  background=[('active', Theme.BG_INPUT)],
                  bordercolor=[('active', Theme.BORDER_FOCUS)])

        # --- Treeview (Token Table) ---
        style.configure("Treeview",
                        background=Theme.BG_PANEL,
                        foreground=Theme.TEXT_MAIN,
                        fieldbackground=Theme.BG_PANEL,
                        font=Theme.FONT_CODE,
                        rowheight=28,
                        borderwidth=0)
        
        style.configure("Treeview.Heading",
                        background=Theme.BG_INPUT,
                        foreground=Theme.TEXT_SECONDARY,
                        font=Theme.FONT_BOLD,
                        borderwidth=0,
                        relief="flat")
        style.map("Treeview.Heading",
                   background=[('active', Theme.BG_INPUT)])

        # --- Scrollbars ---
        style.configure("TScrollbar",
                        background=Theme.BG_INPUT,
                        troughcolor=Theme.BG_MAIN,
                        borderwidth=0,
                        arrowsize=12)
        style.map("TScrollbar",
                  background=[('active', Theme.BORDER_LIGHT)])
