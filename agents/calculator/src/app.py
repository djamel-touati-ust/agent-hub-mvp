import re

_NUM = r"-?\d+(?:\.\d+)?"
_EXPR = re.compile(rf"^\s*({_NUM})\s*([+\-*/])\s*({_NUM})\s*$")

def compute(expr: str) -> str:
    """
    Compute a simple arithmetic expression like:
      '2+2', '7 - 3', '4*1.5', '10/4'

    Returns a string suitable to send back as an A2A text message.
    """
    expr = (expr or "").strip()
    m = _EXPR.fullmatch(expr)
    if not m:
        return "Usage: send text like '2+3', '10 - 4', '6*7', or '8/2'."

    a, op, b = float(m.group(1)), m.group(2), float(m.group(3))
    try:
        if op == "+": val = a + b
        elif op == "-": val = a - b
        elif op == "*": val = a * b
        elif op == "/":
            if b == 0:
                return "Error: division by zero"
            val = a / b
        else:
            return "Unsupported operator"
    except Exception as e:
        return f"Error: {e}"

    return f"{expr} = {int(val) if abs(val - round(val)) < 1e-12 else val}"
