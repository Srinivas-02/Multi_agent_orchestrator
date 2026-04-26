from app.services.tools import calculate_tool

class SimpleAgent:

    async def run(self, exp:str):
        if any (op in exp for op in ["+", "-", "/", "*"]):
            yield "Thinking to use calculate tool"

            Expression = exp.replace("calculate","").strip()

            yield f"Executing calculation tool with expression : {Expression}"

            result = calculate_tool(Expression)

            yield f" Calculating...."

            yield f"Final answer : {result}"

                
        else:            
            yield f"Error in calculating the expression"

        