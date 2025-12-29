import ast
import traceback
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Issue:
    error_type: str
    message: str
    explanation: str
    suggestion: str
    line: Optional[int]
    severity: str = "error"


ERROR_EXPLAIN = {
    "SyntaxError": (
        "There is a Syntax error in the code - Python doesnt understand the structure",
        "Check the ':' or '()' or identations. Very often after new defined function."
    ),
    "IndentationError": (
        "Indent of the code is wrong - Python is very sensitive on this type of error",
        "Check tabs or spaces. Very often after ':' or at the beginning of new line"
    ),
    "NameError": (
        "You use variable or function, that doesnt exist in the code",
        "Check a typo or if the variable or function was even made"
    ),
    "TypeError": (
        "You are trying to combine incompatible types, such as a number and a string",
        "Check the types of variables with function: type('variable')"
    ),
    "ValueError": (
        "Type is correct, but the value doesnt isnt correct",
        "Check the input value or except it with condition"
    ),
    "ZeroDivisionError": (
        "You are trying to divide with a zero.",
        "Before dividing you should check, that the denominator (number you divide with) is not zero."
    ),
    "IndexError": (
        "You are trying to access a list element, outside its valid range",
        "Check the length of the list by function: len('list')."
    ),
    "KeyError": (
        "Dictionary doesnt obtain that key",
        "Check the keys or do this function: dict.get()."
    ),
    "AttributeError": (
        "The object does not have this attribute or method",
        "Check the objects type and the available methods"
    ),
    "EOFError": (
        "Program expected input, but it didnt get any.",
        "Check the use of input() or input of data."
    ),
}


def check_syntax(code: str) -> Optional[Issue]:
    try:
        ast.parse(code)
        return None
    except (SyntaxError, IndentationError) as e:
        error_type = type(e).__name__
        explanation, suggestion = ERROR_EXPLAIN.get(
            error_type,
            ("Syntax error in the code", "Check the code structure")
        )

        return Issue(
            error_type=error_type,
            message=e.msg,
            explanation=explanation,
            suggestion=suggestion,
            line=e.lineno,
        )


def run_code(code: str) -> Optional[Issue]:
    try:
        safe_globals = {
            "__builtins__": {
                "print": print,
                "int": int,
                "float": float,
                "str": str,
                "len": len,
                "range": range,
                "input": input,
            }
        }

        exec(code, safe_globals)
        return None

    except KeyboardInterrupt:
        return Issue(
            error_type="KeyboardInterrupt",
            message="Program was manually stopped",
            explanation="Code run was stopped by an user",
            suggestion="Dont end the program, if it isnt on purpose",
            line=None,
        )

    except Exception as e:
        error_type = type(e).__name__
        explanation, suggestion = ERROR_EXPLAIN.get(
            error_type,
            ("The program went into a error", "Check the error message")
        )

        tb = traceback.extract_tb(e.__traceback__)
        # Use of AI - line --> 115
        line = tb[-1].lineno if tb else None

        return Issue(
            error_type=error_type,
            message=str(e),
            explanation=explanation,
            suggestion=suggestion,
            line=line,
        )


def analyze_code(code: str) -> List[Issue]:
    issues: List[Issue] = []

    syntax_issue = check_syntax(code)
    if syntax_issue:
        issues.append(syntax_issue)
        return issues

    runtime_issue = run_code(code)
    if runtime_issue:
        issues.append(runtime_issue)

    return issues
