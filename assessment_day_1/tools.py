"""
Tools module for the Day 1 Assessment project.
Provides private course fee data lookup and a safe math calculator (no eval).
"""
import ast
import operator

# Private college course-fee database
COURSE_FEES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000,
}

# Supported operators for safe math evaluation
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval_node(node):
    """Recursively evaluates AST nodes safely without raw eval()."""
    if isinstance(node, ast.Expression):
        return _safe_eval_node(node.body)
    elif isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")
    elif isinstance(node, ast.BinOp):
        left = _safe_eval_node(node.left)
        right = _safe_eval_node(node.right)
        op_type = type(node.op)
        if op_type in _OPERATORS:
            return _OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
    elif isinstance(node, ast.UnaryOp):
        operand = _safe_eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _OPERATORS:
            return _OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
    else:
        raise ValueError(f"Unsupported expression syntax: {type(node).__name__}")


def get_course_fee(course_code: str):
    """
    Look up the private tuition fee for a given course code.
    
    Args:
        course_code (str): The code of the course (e.g. CS101, AI202, DS303)
        
    Returns:
        int or str: Fee in Rs. or error string if not found.
    """
    code = str(course_code).strip().upper()
    if code in COURSE_FEES:
        return COURSE_FEES[code]
    return f"Error: Course '{course_code}' not found. Available courses: {list(COURSE_FEES.keys())}"


def calculator(expression: str):
    """
    Safely evaluate arithmetic expressions without using Python eval().
    
    Args:
        expression (str): Math expression (e.g., '(12000 + 18000) * 0.9')
        
    Returns:
        int, float, or str: Calculated result or error string.
    """
    try:
        # Clean currency characters or extraneous formatting
        clean_expr = str(expression).replace(",", "").replace("Rs.", "").replace("Rs", "").strip()
        parsed_ast = ast.parse(clean_expr, mode="eval")
        result = _safe_eval_node(parsed_ast)
        if isinstance(result, float) and result.is_integer():
            return int(result)
        return result
    except Exception as err:
        return f"Error evaluating expression '{expression}': {err}"


# JSON Schema tool definitions for LLM tool calling
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": "Retrieves the private tuition fee (in Rs.) for a course code (CS101, AI202, DS303).",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "The course code to look up, e.g., CS101, AI202, DS303."
                    }
                },
                "required": ["course_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluates math expressions safely (addition, subtraction, multiplication, division, scholarship percentages).",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression string to evaluate, e.g., '(12000 + 18000) * 0.9' or '15000 - 12000'."
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# Map tool names to python functions for agent execution
TOOL_MAP = {
    "get_course_fee": get_course_fee,
    "calculator": calculator,
}
