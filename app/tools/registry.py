from app.tools.calculator import calculator
from app.tools.string_tools import reverse_text, uppercase_text
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
    },
    "reverse_text": {
        "function" : reverse_text,
        "declaration" : {
            "name" : "reverse_text",
            "description" : "Reverses a given text",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "text" : {"type" : "string",}
                },
                "required" : ["text"]
            }
        }
    },
    "uppercase_text" : {
        "function" : uppercase_text,
        "declaration": {
            "name" : "uppercase_text",
            "description" : "Convert given text into uppercase",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "text" : { "type" : "string"},
                },
                "required" : ["text"]
            }
        }
    }
}

def get_tool_declarations():
    return [tool["declaration"] for tool in TOOLS.values()]
