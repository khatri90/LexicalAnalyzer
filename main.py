import sys
import os

# Ensure src is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.view.main_window import MainWindow

def main():
    """
    Main entry point for the ProLexer Studio application.
    """
    app = MainWindow()
    app.run()

if __name__ == "__main__":
    main()
