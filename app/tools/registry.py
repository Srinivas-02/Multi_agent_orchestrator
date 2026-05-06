from app.tools.calculator import calculator
from app.tools.string_tools import reverse_text, uppercase_text
from app.tools.text_analyzer import analyze_text
from app.tools.unit_converter import convert_units


TOOLS = {
    "calculator" : {
        "function": calculator,
        "declaration": {
            "name" : "calculator",
            "description" : "Evaluate a mathematical expression. Supports +, -, *, /, //, %, **, parentheses, unary signs, constants pi/e/tau, and functions like sqrt, sin, cos, tan, log, log10, abs, round, min, max, pow, ceil, and floor.",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "expression" : {
                        "type" : "string",
                        "description" : "Math expression like sqrt(16) + 5 * (10 - 3) or sin(pi / 2)"
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
    },
    "convert_units": {
        "function": convert_units,
        "declaration": {
            "name": "convert_units",
            "description": "Convert numeric values between supported length and mass units.",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {
                        "type": "number",
                        "description": "Numeric value to convert"
                    },
                    "from_unit": {
                        "type": "string",
                        "description": "Source unit: mm, cm, m, km, in, ft, yd, mi, mg, g, kg, oz, or lb"
                    },
                    "to_unit": {
                        "type": "string",
                        "description": "Target unit: mm, cm, m, km, in, ft, yd, mi, mg, g, kg, oz, or lb"
                    }
                },
                "required": ["value", "from_unit", "to_unit"]
            }
        }
    },
    "analyze_text": {
        "function": analyze_text,
        "declaration": {
            "name": "analyze_text",
            "description": "Analyze text and return character, word, sentence, and line counts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to analyze"
                    }
                },
                "required": ["text"]
            }
        }
    }
}

def get_tool_declarations():
    return [tool["declaration"] for tool in TOOLS.values()]
