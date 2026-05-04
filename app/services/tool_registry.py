from app.services.tools import calculator

TOOLS = {
    "calculator" : {
        "function": calculator,
        "declaration": {
            "name" : "calculator",
            "description" : "Evaluate a mathematical expression",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "expression" : {
                        "type" : "string",
                        "description" : "Math expression like 5 * 10"
                    }
                },
                "required" : ["expression"]
            }
        }
    }
}

def get_tool_declarations():
    return [tool["declaration"] for tool in TOOLS.values()]