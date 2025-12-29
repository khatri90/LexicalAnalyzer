import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from .theme import Theme
from .components import CodeEditor, TokenTable
from ..model.lexer import LexicalAnalyzer
from ..model.token import TokenType

class MainWindow:
    """
    The main application controller and view composer.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ProLexer Studio")
        self.root.geometry("1400x800")
        
        # Apply Theme
        Theme.configure_style(self.root)
        self.root.configure(bg=Theme.BG_MAIN)
        
        try:
            self.root.iconbitmap("icon.ico")
        except Exception:
            pass 
            
        self.analyzer = LexicalAnalyzer()
        
        self._setup_layout()
        
    def _setup_layout(self):
        # --- Top Bar ---
        top_bar = ttk.Frame(self.root, style="Card.TFrame", padding=(20, 10))
        top_bar.pack(side="top", fill="x")
        
        # Title
        title_lbl = tk.Label(top_bar, text="Lexical Analyzer", 
                             font=Theme.FONT_HEADER, 
                             bg=Theme.BG_PANEL, 
                             fg=Theme.TEXT_MAIN)
        title_lbl.pack(side="left")
        
        # Action Buttons
        btn_frame = ttk.Frame(top_bar, style="Card.TFrame")
        btn_frame.pack(side="right")
        
        ttk.Button(btn_frame, text="Load Source", command=self.load_file).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_all).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Analyze Code", command=self.run_analysis, style="Primary.TButton").pack(side="left", padx=5)
        
        # --- Main Content (Split Pane) ---
        content_pane = ttk.PanedWindow(self.root, orient="horizontal")
        content_pane.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left Panel: Editor
        left_frame = ttk.Frame(content_pane, style="Card.TFrame", padding=1)
        self.editor = CodeEditor(left_frame)
        self.editor.pack(fill="both", expand=True)
        content_pane.add(left_frame, weight=1)
        
        # Right Panel: Results
        right_frame = ttk.Frame(content_pane, style="Card.TFrame", padding=1)
        
        # Stats Bar
        self.stats_label = tk.Label(right_frame, text="Ready", font=Theme.FONT_MAIN, 
                                    bg=Theme.BG_PANEL, fg=Theme.TEXT_SECONDARY, anchor="w")
        self.stats_label.pack(fill="x", padx=10, pady=5)
        
        # Table
        self.token_table = TokenTable(right_frame)
        self.token_table.pack(fill="both", expand=True)
        
        content_pane.add(right_frame, weight=1)
        
        # --- Status Bar ---
        self.status_bar = tk.Label(self.root, text="System Ready", bd=0, anchor="w", 
                                   bg=Theme.PRIMARY, fg=Theme.PRIMARY_FG, 
                                   font=("Segoe UI", 9), padx=10, pady=5)
        self.status_bar.pack(side="bottom", fill="x")

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("C Files", "*.c"), ("All Files", "*.*")])
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.editor.delete("1.0", tk.END)
                    self.editor.insert("1.0", content)
                self.status_bar.config(text=f"Loaded: {path}")
            except Exception as e:
                messagebox.showerror("Load Error", str(e))

    def clear_all(self):
        self.editor.delete("1.0", tk.END)
        for item in self.token_table.get_children():
            self.token_table.delete(item)
        self.stats_label.config(text="Ready", fg=Theme.TEXT_SECONDARY)
        self.status_bar.config(text="Cleared workspace")

    def run_analysis(self):
        code = self.editor.get("1.0", tk.END)
        if not code.strip():
            messagebox.showwarning("Empty", "No code to analyze.")
            return

        # Clear previous
        for item in self.token_table.get_children():
            self.token_table.delete(item)
            
        # Run
        try:
            tokens = self.analyzer.analyze(code)
            errors = self.analyzer.errors
            
            # Populate Table
            for token in tokens:
                tag = ''
                if token.type in (TokenType.INVALID, TokenType.UNCLOSED_STRING, TokenType.UNCLOSED_COMMENT):
                    tag = 'error'
                    
                self.token_table.insert("", "end", values=(
                    token.index,
                    token.type.value,
                    token.value,
                    token.line,
                    token.column
                ), tags=(tag,))
            
            # Update Status
            stats = f"Tokens: {len(tokens)} | Errors: {len(errors)}"
            self.stats_label.config(text=stats, fg=Theme.TOKEN_ERROR if errors else Theme.TOKEN_NUMBER)
            
            if errors:
                self.status_bar.config(text=f"Analysis completed with {len(errors)} errors.", bg=Theme.TOKEN_ERROR)
                messagebox.showwarning("Analysis Issues", "\n".join(errors))
            else:
                self.status_bar.config(text="Analysis completed successfully.", bg=Theme.PRIMARY)
                
        except Exception as e:
            messagebox.showerror("System Error", f"An unexpected error occurred: {e}")

    def run(self):
        self.root.mainloop()
