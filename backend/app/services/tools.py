import ast
import csv
import operator
from io import StringIO


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def calculate(expression: str) -> str:
    def eval_node(node):
        if isinstance(node, ast.Expression):
            return eval_node(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](eval_node(node.left), eval_node(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](eval_node(node.operand))
        raise ValueError("Only basic arithmetic is supported")

    return f"{float(eval_node(ast.parse(expression, mode='eval'))):g}"


def summarize_csv(csv_text: str) -> str:
    rows = list(csv.DictReader(StringIO(csv_text.strip())))
    if not rows:
        return "CSV has 0 rows."
    return f"CSV has {len(rows)} rows and columns: {', '.join(rows[0].keys())}."


def planning_checklist(goal: str) -> list[str]:
    return [
        f"Clarify the outcome for: {goal}",
        "Retrieve the most relevant project documents",
        "Choose any required tool calls",
        "Draft the final answer with sources",
        "Review for missing assumptions or errors",
    ]
