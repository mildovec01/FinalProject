# Code Tutor – Runtime & Syntax Error Explainer

### Video: [Click here](https://www.youtube.com/watch?v=oKsMBicdNMY)

## Description

Code Tutor is a web-based educational application created as a CS50 final project. The purpose of the project is to help beginner Python programmers understand **real Python errors** that occur when code is written incorrectly. Instead of focusing on style, formatting, or advanced best practices, the application concentrates exclusively on **syntax errors and runtime exceptions** that Python itself raises.

Many beginners struggle with error messages such as `SyntaxError`, `TypeError`, or `ValueError`. While Python provides these messages, they are often short, technical, and difficult to understand for someone who is still learning. Code Tutor aims to act as an intermediate layer between Python’s error output and the learner, translating errors into clear explanations and practical suggestions.

The project intentionally avoids artificial intelligence and complex static analysis tools. All logic is implemented using standard Python features. This design choice keeps the application transparent and ensures that the developer fully understands how every part of the system works, which aligns well with the educational goals of CS50.

## How the application works

The user interacts with Code Tutor through a simple web interface. Python code can be pasted into a text editor and analyzed by pressing a single button. The analysis process is divided into two clearly separated phases.

### Syntax analysis

The first phase checks the code for syntax and indentation errors. This is done using Python’s built-in `ast` module. Syntax errors are problems that prevent the program from running at all, such as missing colons, invalid indentation, or unclosed parentheses.

If a syntax error is detected, the application immediately stops further processing. The error type, message, and line number are extracted and converted into a beginner-friendly explanation. This mirrors Python’s real behavior, where execution does not continue if the syntax is invalid.

### Runtime execution

If the syntax is valid, the application proceeds to the second phase, which executes the code in a **restricted and controlled environment**. This execution is wrapped in a `try/except` block to catch runtime exceptions.

Runtime errors occur while the program is running. These include errors such as dividing by zero, using incompatible data types, accessing elements outside a list’s range, or referencing variables that do not exist. When such an error occurs, Code Tutor captures the exception type, error message, and traceback information to identify the line where the problem happened.

Each runtime error is then mapped to a predefined explanation and suggestion written specifically for beginners.

## Supported error types

The application focuses on a limited but meaningful set of Python errors that beginners encounter most frequently:

- SyntaxError  
- IndentationError  
- NameError  
- TypeError  
- ValueError  
- ZeroDivisionError  
- IndexError  
- KeyError  
- AttributeError  
- EOFError  
- KeyboardInterrupt  

This selection was chosen intentionally. Instead of overwhelming users with rare or advanced errors, Code Tutor concentrates on mistakes that naturally occur when learning Python basics such as variables, functions, lists, dictionaries, and arithmetic operations.

## Data storage and history

Each analysis is stored in an SQLite database. For every analyzed code snippet, the application saves the timestamp, programming language, and the original code. Detected issues are stored in a separate table and linked to their corresponding analysis.

This allows users to revisit previous analyses through the history page. The database design demonstrates relational data modeling and persistent storage, which are core concepts covered in CS50.

SQLite was chosen because it is lightweight, requires no external server, and is well suited for local applications and educational projects.

## Project Structure

I used AI for this structure to be more well arranged and visualy better.

project/
├── app.py
├── helpers.py
├── requirements.txt
├── README.md
├── data/
│ └── codetutor.db
├── templates/
│ ├── layout.html
│ ├── index.html
│ ├── report.html
│ └── history.html
├── static/
│ └── styles.css
| └── script.js
└── tests/
└── samples.py

### File overview

- **app.py**  
  The main Flask application. It defines routes, handles form submissions, manages database connections, and renders templates.

- **helpers.py**  
  Contains all analysis logic. This includes syntax checking, safe execution of user code, exception handling, and mapping errors to explanations.

- **templates/**  
  HTML templates rendered using Jinja2. Template inheritance is used to keep the layout consistent and avoid duplication.

- **static/styles.css**  
  Styling for the user interface. The design focuses on readability and clarity rather than visual complexity.

- **static/script.js**
  Didnt use it, it is possible to make code in the future for better highlight.

- **data/codetutor.db**  
  SQLite database storing analyses and detected issues.

- **tests/samples.py**  
  A collection of intentionally incorrect Python code examples used for testing and demonstration.

## Design decisions

A major design decision was to exclude linters and style checkers. While such tools are useful for experienced developers, they often produce warnings that are confusing or irrelevant for beginners. Code Tutor focuses only on errors that Python actually raises during parsing or execution.

Another important choice was to handle only the first error encountered. This matches Python’s real execution model and prevents users from being overwhelmed by multiple error messages at once.

The application also restricts the execution environment to avoid unsafe operations. Only a small subset of built-in functions is allowed, which is sufficient for beginner-level code while reducing potential risks.

## Limitations

Code Tutor is intended for educational and local use. It is not designed as a secure sandbox for executing untrusted code in a production environment. Interactive input handling is limited, and only one error is reported per analysis.

Despite these limitations, the application effectively demonstrates the core concepts of syntax parsing, exception handling, database usage, and web application development.

## Future improvements

Potential future extensions include:
- step-by-step execution visualization
- additional explanations with examples
- support for more programming languages
- a standalone desktop version
- enhanced handling of interactive programs

## Conclusion

Code Tutor is a focused educational tool that helps beginners understand Python errors in a practical and approachable way. By explaining real syntax and runtime errors without unnecessary complexity, the project aims to make debugging less intimidating and more educational for new programmers.
