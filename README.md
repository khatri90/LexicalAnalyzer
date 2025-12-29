# ProLexer Studio

A professional-grade Lexical Analysis tool for C-like languages, built with Python and Tkinter.

![ProLexer Screenshot](placeholder_screenshot.png)

## Features

- **Modular Architecture**: Built using a proper Model-View-Controller (MVC) separation.
- **Robust Tokenization**: Accurate detection of keywords, identifiers, numbers, operators, strings, and delimiters.
- **Error Reporting**: Real-time detection of unclosed strings and invalid number formats.
- **Modern UI**: A clean, professional user interface with a custom theme and responsive layout.
- **Type Safety**: Fully type-hinted codebase for better maintainability.

## Installation

No external dependencies are required. This application runs on standard Python 3.

```bash
# Clone the repository
git clone https://github.com/yourusername/pro-lexer.git

# Navigate to the directory
cd ProfessionalLexer
```

## Usage

Run the application using the main entry point:

```bash
python main.py
```

1. Click **Load Source** to open a C or text file.
2. Click **Analyze Code** to generate tokens.
3. View the results in the interactive table or check the status bar for errors.

## Project Structure

```text
ProfessionalLexer/
├── main.py                 # Application Entry Point
├── src/
│   ├── model/              # Core Logic
│   │   ├── token.py        # Token Data Definitions
│   │   └── lexer.py        # Lexical Analysis Engine
│   └── view/               # User Interface
│       ├── theme.py        # Visual Theme & Constants
│       ├── components.py   # Custom Styled Widgets
│       └── main_window.py  # Main GUI Controller
```

## License

MIT License - Free for educational and professional use.
