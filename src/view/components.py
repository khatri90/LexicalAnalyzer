import tkinter as tk
from tkinter import ttk, scrolledtext
from .theme import Theme

class ModernButton(tk.Button):
    """
    A unified button style consistent across the application.
    """
    def __init__(self, parent, text, command=None, is_primary=False, **kwargs):
        bg_color = Theme.PRIMARY if is_primary else "white"
        fg_color = Theme.TEXT_WHITE if is_primary else Theme.TEXT_MAIN
        
        super().__init__(parent, text=text, command=command,
                         bg=bg_color, fg=fg_color,
                         relief="flat", bd=0,
                         padx=15, pady=5,
                         cursor="hand2",
                         font=Theme.FONT_BOLD if is_primary else Theme.FONT_MAIN,
                         activebackground=Theme.PRIMARY_HOVER if is_primary else "#e2e8f0",
                         activeforeground=fg_color,
                         **kwargs)

class CodeEditor(scrolledtext.ScrolledText):
    """
    A code editor widget with line numbering gutter placeholders involved (simplified for this task).
    Visual enhancements: minimalist border, code font.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 
                         font=Theme.FONT_CODE, 
                         bg=Theme.BG_INPUT, 
                         fg=Theme.TEXT_MAIN,
                         relief="flat", 
                         padx=5, pady=5,
                         **kwargs)
        self.configure(selectbackground=Theme.PRIMARY, selectforeground="white")

class TokenTable(ttk.Treeview):
    """
    A styled Treeview for displaying tokens.
    """
    def __init__(self, parent, **kwargs):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure Treeview colors to match theme
        style.configure("Treeview",
                        background=Theme.BG_PANEL,
                        foreground=Theme.TEXT_MAIN,
                        rowheight=25,
                        fieldbackground=Theme.BG_PANEL,
                        font=Theme.FONT_CODE)
        
        style.configure("Treeview.Heading",
                        background=Theme.BG_MAIN,
                        foreground=Theme.TEXT_MAIN,
                        relief="flat",
                        font=Theme.FONT_BOLD)
        
        style.map("Treeview", background=[('selected', Theme.PRIMARY)])
        
        super().__init__(parent, columns=("Index", "Type", "Value", "Line", "Col"), show="headings", **kwargs)
        
        self.heading("Index", text="#")
        self.column("Index", width=40, anchor="center")
        
        self.heading("Type", text="Token Type")
        self.column("Type", width=120, anchor="w")
        
        self.heading("Value", text="Value")
        self.column("Value", width=200, anchor="w")
        
        self.heading("Line", text="Ln")
        self.column("Line", width=40, anchor="center")
        
        self.heading("Col", text="Col")
        self.column("Col", width=40, anchor="center")
        
        # Striped rows tag
        self.tag_configure('even', background=Theme.BG_INPUT)
        self.tag_configure('error', background="#fee2e2", foreground="#ef4444")
