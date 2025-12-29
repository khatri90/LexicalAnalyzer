import tkinter as tk
from tkinter import ttk
from .theme import Theme

class TextLineNumbers(tk.Canvas):
    """
    A canvas to display line numbers for a text widget.
    """
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''Redraw line numbers'''
        self.delete("all")
        if not self.textwidget:
            return

        i = self.textwidget.index("@0,0")
        while True:
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(width - 5, y, anchor="ne",
                             text=linenum,
                             fill=Theme.TEXT_SECONDARY,
                             font=Theme.FONT_CODE)
            i = self.textwidget.index("%s+1line" % i)

# Helper for width of linenumber canvas
width = 40

class CodeEditor(tk.Frame):
    """
    A composite widget with line numbers and a text editor.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=Theme.BG_INPUT, bd=1, relief="solid")
        
        self.text = tk.Text(self,
                            font=Theme.FONT_CODE,
                            bg=Theme.BG_INPUT,
                            fg=Theme.TEXT_MAIN,
                            relief="flat",
                            bd=0,
                            undo=True,
                            wrap="none")  # No wrap for code
        
        self.linenumbers = TextLineNumbers(self, width=width, bg=Theme.BG_MAIN, bd=0, highlightthickness=0)
        self.linenumbers.attach(self.text)
        
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.hsb = ttk.Scrollbar(self, orient="horizontal", command=self.text.xview)
        
        self.text.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        
        # Grid Layout
        self.linenumbers.grid(row=0, column=0, sticky="ns")
        self.text.grid(row=0, column=1, sticky="nsew")
        self.vsb.grid(row=0, column=2, sticky="ns")
        self.hsb.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Events
        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)
        self.text.bind("<KeyRelease>", self._on_change)
        self.text.bind("<MouseWheel>", self._on_change)
        self.text.bind("<Button-1>", self._on_change)
        
        # Selection Style
        self.text.configure(selectbackground=Theme.PRIMARY, selectforeground=Theme.PRIMARY_FG)

    def _on_change(self, event=None):
        self.linenumbers.redraw()

    # Proxy methods to behave like a Text widget
    def get(self, *args, **kwargs): return self.text.get(*args, **kwargs)
    def insert(self, *args, **kwargs): 
        self.text.insert(*args, **kwargs)
        self._on_change()
    def delete(self, *args, **kwargs): 
        self.text.delete(*args, **kwargs)
        self._on_change()
    def see(self, *args): self.text.see(*args)


class TokenTable(tk.Frame):
    """
    A Token Table with integrated scrollbar.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=Theme.BG_PANEL)
        
        self.tree = ttk.Treeview(self, columns=("Index", "Type", "Value", "Line", "Col"), show="headings")
        
        # Scrollbar
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        
        # Layout
        self.tree.pack(side="left", fill="both", expand=True)
        self.vsb.pack(side="right", fill="y")
        
        # Config Columns
        self.tree.heading("Index", text="#")
        self.tree.column("Index", width=50, anchor="center")
        
        self.tree.heading("Type", text="Token Type")
        self.tree.column("Type", width=150, anchor="w")
        
        self.tree.heading("Value", text="Value")
        self.tree.column("Value", width=250, anchor="w")
        
        self.tree.heading("Line", text="Ln")
        self.tree.column("Line", width=60, anchor="center")
        
        self.tree.heading("Col", text="Col")
        self.tree.column("Col", width=60, anchor="center")
        
        # Tags for styling
        self.tree.tag_configure('error', background="#fee2e2", foreground="#ef4444")
        
    # Proxy methods
    def get_children(self): return self.tree.get_children()
    def delete(self, item): self.tree.delete(item)
    def insert(self, parent, index, iid=None, **kwargs): return self.tree.insert(parent, index, iid, **kwargs)
