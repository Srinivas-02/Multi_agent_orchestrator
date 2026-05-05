import ast, operator
def calculator(expression:str) -> str:
    ops = {
        ast.Add : operator.add,
        ast.Sub : operator.sub,
        ast.Mult : operator.mul,
        ast.Div : operator.truediv,   
    }

    def eval_expr(node):
        if isinstance(node, ast.BinOp):
            return ops[type(node.op)](eval_expr(node.left), eval_expr(node.right))
        if isinstance(node, ast.Constant):
            return node.value
        else:
            raise ValueError("Invalid Expression")
        
    tree = ast.parse(expression, mode="eval")
    return str(eval_expr(tree.body))