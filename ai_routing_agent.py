import os
import re 
import json
import argparse
from typing import List, Dict, Any
from dataclasses import dataclass
from tools.multiplication_tool import MultiplicationTool, MultiplicationParams
from tools.vowel_counter import VowelCounter, VowelCountParams
from tools.text_summarizer import summarize
from tools.text_funifier import funify
from dotenv import find_dotenv, load_dotenv
import google.generativeai as genai

load_dotenv(find_dotenv())
API_KEY = os.environ['GEMINI_API_KEY']

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@dataclass
class ToolSpec:
    name: str
    description: str
    parameters: Dict[str, Dict[str, Any]]

# Defining tools
TOOL_SPECS = [
    ToolSpec(
        name="multiplication_tool",
        description="Multiplies a list of numbers together",
        parameters={
            "numbers": {
                "type": "array",
                "items": {"type": "number"},
                "description": "The numbers to multiply"
            }
        }
    ),
    ToolSpec(
        name="vowel_counter",
        description="Counts the number of vowels in a given text",
        parameters={
            "text": {
                "type": "string",
                "description": "The text to count vowels in"
            }
        }
    ),
    ToolSpec(
        name="text_summarizer",
        description="Summarizes the given text",
        parameters={
            "text": {
                "type": "string",
                "description": "The text to summarize"
            }
        }
    ),
    ToolSpec(
        name="text_funifier",
        description="Makes the given text funnier",
        parameters={
            "text": {
                "type": "string",
                "description": "The text to make funnier"
            }
        }
    )
]

class AIRoutingAgent:
    def __init__(self):
        self.tools = {
            "multiplication_tool": MultiplicationTool(),
            "vowel_counter": VowelCounter(),
            # Text summarizer and funifier are function-based, not class-based
        }
        self.function_definitions = self._create_function_definitions()

    def _create_function_definitions(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": spec.name,
                "description": spec.description,
                "parameters": {
                    "type": "object",
                    "properties": spec.parameters,
                    "required": list(spec.parameters.keys())
                }
            }
            for spec in TOOL_SPECS
        ]

    def _get_tool_call(self, prompt: str) -> Dict[str, Any]:
        function_definitions_str = json.dumps(self.function_definitions, indent=2)
        
        response = model.generate_content(
            f"""Based on this request: '{prompt}', determine which tool to use and what parameters to extract. 
            Respond with a JSON object containing 'name' (tool name) and 'parameters' (tool parameters).
            
            Available tools: {function_definitions_str}
            
            Example response format:
            {{
                "name": "multiplication_tool",
                "parameters": {{
                    "numbers": [5, 6]
                }}
            }}""",
            generation_config={
                "temperature": 0.1,
                "max_output_tokens": 100,
            }
        )
        
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    return {"error": f"Failed to parse JSON from response: {response.text}"}
            else:
                return {"error": f"No JSON found in response: {response.text}"}

    def route(self, prompt: str) -> str:
        tool_call = self._get_tool_call(prompt)
        
        if "error" in tool_call:
            return f"Error: {tool_call['error']}"
        
        if "name" not in tool_call or "parameters" not in tool_call:
            return f"Invalid tool call format: {tool_call}"
        
        print(f"Tool to be called: {tool_call['name']}")
        print(f"Parameters: {json.dumps(tool_call['parameters'], indent=2)}")
        
        try:
            if tool_call["name"] == "multiplication_tool":
                params = MultiplicationParams(numbers=tool_call["parameters"]["numbers"])
                result = self.tools["multiplication_tool"].multiply(params)
                return f"The product is {result}"
            
            elif tool_call["name"] == "vowel_counter":
                params = VowelCountParams(text=tool_call["parameters"]["text"])
                result = self.tools["vowel_counter"].count_vowels(params)
                return f"The number of vowels is {result}"
            
            elif tool_call["name"] == "text_summarizer":
                result = summarize(tool_call["parameters"]["text"])
                return f"Summary: {result}"
            
            elif tool_call["name"] == "text_funifier":
                result = funify(tool_call["parameters"]["text"])
                return f"Funified text: {result}"
            
            else:
                return f"Unknown tool: {tool_call['name']}"
        
        except Exception as e:
            return f"Error executing tool: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="AI Routing Agent CLI")
    parser.add_argument('prompt', nargs='?', type=str, help='User prompt')
    args = parser.parse_args()

    agent = AIRoutingAgent()
    if args.prompt:
        response = agent.route(args.prompt)
        print(f"Result: {response}")
    else:
        print("Welcome to the AI Routing Agent CLI! Type 'exit' or 'quit' to quit.")
        while True:
            prompt = input("Enter your prompt: ")
            print('----------------------------------------------------------------')
            if prompt.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            response = agent.route(prompt)
            print('----------------------------------------------------------------')
            print(f"Result: {response}")
            print('----------------------------------------------------------------')

if __name__ == "__main__":
    main()