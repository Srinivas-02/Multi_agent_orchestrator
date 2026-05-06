import ast
import math
import operator


def calculator(expression: str) -> str:
    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    unary_ops = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    functions = {
        "abs": abs,
        "ceil": math.ceil,
        "floor": math.floor,
        "round": round,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "log": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "pow": pow,
        "min": min,
        "max": max,
    }

    constants = {
        "pi": math.pi,
        "e": math.e,
        "tau": math.tau,
    }

    def eval_expr(node):
        if isinstance(node, ast.BinOp):
            if type(node.op) not in ops:
                raise ValueError("Unsupported operator")
            return ops[type(node.op)](eval_expr(node.left), eval_expr(node.right))

        if isinstance(node, ast.UnaryOp):
            if type(node.op) not in unary_ops:
                raise ValueError("Unsupported unary operator")
            return unary_ops[type(node.op)](eval_expr(node.operand))

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in functions:
                raise ValueError("Unsupported function")
            args = [eval_expr(arg) for arg in node.args]
            if node.keywords:
                raise ValueError("Keyword arguments are not supported")
            return functions[node.func.id](*args)

        if isinstance(node, ast.Name):
            if node.id not in constants:
                raise ValueError("Unsupported constant")
            return constants[node.id]

        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Invalid expression")

    tree = ast.parse(expression, mode="eval")
    return str(eval_expr(tree.body))
