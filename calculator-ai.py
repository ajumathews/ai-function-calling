import ollama

def add_two_numbers(a: int, b: int) -> int:
  return a + b

def subtract_two_numbers(a: int, b: int) -> int:
  return a - b


add_two_numbers_tool = {
  'type': 'function',
  'function': {
    'name': 'add_two_numbers',
    'description': 'Add two numbers',
    'parameters': {
      'type': 'object',
      'required': ['a', 'b'],
      'properties': {
        'a': {'type': 'integer', 'description': 'The first number'},
        'b': {'type': 'integer', 'description': 'The second number'},
      },
    },
  },
}


subtract_two_numbers_tool = {
  'type': 'function',
  'function': {
    'name': 'subtract_two_numbers',
    'description': 'Subtract two numbers',
    'parameters': {
      'type': 'object',
      'required': ['a', 'b'],
      'properties': {
        'a': {'type': 'integer', 'description': 'The first number'},
        'b': {'type': 'integer', 'description': 'The second number'},
      },
    },
  },
}

available_functions = {
  'add_two_numbers': add_two_numbers,
  'subtract_two_numbers': subtract_two_numbers,
}


prompt = 'Substract 10 from 3'
print('Prompt:', prompt)

response = ollama.chat(
    'llama3.1',
    messages=[{'role': 'user', 'content': prompt}],
    tools=[add_two_numbers, subtract_two_numbers]
)

if response.message.tool_calls:
    for tool in response.message.tool_calls:
        if function_to_call := available_functions.get(tool.function.name):
            print('Calling function:', tool.function.name)
            print('Arguments:', tool.function.arguments)
            arguments = {k: int(v) for k, v in tool.function.arguments.items()}
            print('Function output:', function_to_call(**arguments))
        else:
            print('Function', tool.function.name, 'not found')