import ast
import json
import subprocess
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

@dataclass
class Issue:
    tool: str
    code: str
    message: str
    explanation: str
    suggestion: str
    line: int
    col: int
    end_line: Optional[int] = None
    end_col: Optional[int] = None
    severity: str = "warning"

RUFF_EXPLAIN: Dict[str, Dict[str, str]] = {
    # Use of AI - lines --> 22, 27, 32, 37
    "F401": {
        "explanation": "You are importing something, you didnt use. It is not a mistake, but it is sure waste of code.",
        "suggestion": "Delete that import or just use it."
    },
    
    "F841": {
        "explanation": "Variable gets the value, but it is never used. Usually marked as bug or waste of code.",
        "suggestion": "Use that variable or just delete it. If it is on purpose, use '_' after the variable, example: --> 'x_ = 10'"
    },

    "E722": {
        "explanation": "You are getting 'except: ' without a type of exception. Thats dangerous, because it hides KeyboardInterrupt or SystemExit",
        "suggestion": "Use the type of exception for example --> 'except ValueError:' or at least --> 'except Exception' if you are unsure of type of exception"
    },

    "E501": {
        "explanation": "Line of code is too long - readability goes down and it is worse to keep it together",
        "suggestion": "Try to use variables to minimize the line."
    }
}  

def analyze_python_syntax(code: str) -> List[Issue]:
    try:
        ast.parse(code)
        return []
    except SyntaxError as e:
        # Use of AI - lines --> 49, 50
        line = int(getattr(e, "lineno", 1) or 1)
        col = int(getattr(e, "offset", 0) or 0)
        msg = (e.msg or "Syntax error").strip()
        return [Issue(
            tool="python",
            code="SYNTAX",
            message=msg,
            explanation="Python parser got a failure of syntax. It does mean that often ':', '()', '\"', or 'just indentation'",
            suggestion="Control that line --> especially to 'if/for/def' at the end of the line it needs to have ':' or look for '()' or indents",
            line=line,
            col=col,
            severity="error"
        )]
    
def run_ruff(code: str) -> List[Issue]:
    try:
        proc = subprocess.run(
            #Use of AI - line --> 67
            ["ruff", "check", "-", "--format", "json"],
            input=code.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except FileNotFoundError:
        return [Issue(
            tool="ruff",
            code="RUFF_NOT_FOUND",
            message="Ruff is not installed or is not in PATH",
            explanation="Lint engine misses, i can do only syntax check",
            suggestion="Install 'ruff' and run the app from the same enviroment",
            line=1,
            col=0,
            severity="error",
        )]

    if proc.returncode not in (0, 1):
        err = proc.stderr.decode("utf-8", errors="replace").strip()
        return [Issue(
            tool="ruff",
            code="RUFF_ERROR",
            message="Ruff analyze failed",
            explanation="Ruff ran into an internal error or wrong input",
            suggestion=f"Try it again. Detail: {err[:200]}",
            line=1,
            col=0,
            severity="error",
        )]

    out = proc.stdout.decode("utf-8", errors="replace").strip()
    if not out:
        return []

    # Use of AI - lines --> 103, 104
    data: List[Dict[str, Any]] = json.loads(out)
    issues: List[Issue] = []

    for item in data:
        code_id = item.get("code", "RUFF")
        msg = (item.get("message", "Issue") or "").strip()

        loc = item.get("location") or {}
        end_loc = item.get("end_location") or {}

        line = int(loc.get("row", 1))
        col = int(loc.get("column", 0))
        end_line = end_loc.get("row")
        end_col = end_loc.get("column")

        meta = RUFF_EXPLAIN.get(code_id)
        if meta:
            explanation = meta["explanation"]
            suggestion = meta["suggestion"]
        else:
            # Use of AI - lines --> 124, 125
            explanation = "Lint tool found problem with style. It doesnt need to break the program, but often it is bug or unreadable code"
            suggestion = "Read a warning a repair the code by it. If it is false-positive, you can turn off the rule later."  

        severity = "warning"
        if code_id.startswith(("F", "E9")):
            severity = "error"
        elif code_id.startswith(("E", "W")):
            severity = "warning"
        else:
            severity = "info"

        issues.append(Issue(
            tool="ruff",
            code=code_id,
            message=msg,
            explanation=explanation,
            suggestion=suggestion,
            line=line,
            col=col,
            end_line=int(end_line) if end_line is not None else None,
            end_col=int(end_col) if end_col is not None else None,
            severity=severity,
        ))
    return issues

def analyze_code(code: str) -> List[Issue]:
    issues: List[Issue] = []
    issues.extend(analyze_python_syntax(code))
    issues.extend(run_ruff(code))

    severity_order = {"error": 0, "warning": 1, "info": 2}
    #Use of AI - line --> 156
    issues.sort(key=lambda x: (severity_order.get(x.severity, 9), x.line, x.col))
    return issues
                          