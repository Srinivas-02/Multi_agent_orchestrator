def calculate_tool(expression: str) -> str:
    try:
        ans = eval(expression)
        return str(ans)
    except Exception as e:
        return f"Error : {str(e)}"