from ollama import Client
import yfinance as yf
from typing import Dict, Any, Callable

ollama_server_url = "http://192.168.1.207:11434"
client = Client(host=ollama_server_url)

def get_current_stock_price(symbol) -> float:
    stock = yf.Ticker(symbol)
    todays_data = stock.history(period='1d')    
    return round(todays_data['Close'].iloc[0], 2)

def get_20_day_moving_average(symbol) -> float:
    stock = yf.Ticker(symbol)
    history_data = stock.history(period='30d')
    dma_20 = history_data['Close'].rolling(window=20).mean().iloc[-1]
    return round(dma_20, 2)


get_current_stock_price_tool = {
    'type': 'function',
    'function': {
        'name': 'get_current_stock_price',
        'description': 'Get the current stock price for any symbol',
        'parameters': {
            'type': 'object',
            'required': ['symbol'],
            'properties': {
                'symbol': {'type': 'string', 'description': 'The stock symbol eg. AAPL'},
            },
        },
    },
}

get_20_day_moving_average_tool = {
    'type': 'function',
    'function': {
        'name': 'get_20_day_moving_average',
        'description': 'Get the 20 day moving average stock price for any symbol',
        'parameters': {
            'type': 'object',
            'required': ['symbol'],
            'properties': {
                'symbol': {'type': 'string', 'description': 'The stock symbol eg. AAPL'},
            },
        },
    },
}

available_functions: Dict[str, Callable] = {
    'get_current_stock_price': get_current_stock_price,
    'get_20_day_moving_average': get_20_day_moving_average
}

system_prompt = """
You are a helpful assistant that can only provide accurate responses by using the available tools. 
Do not generate hallucinated content or provide answers that cannot be derived from the tools.
If a valid function is available and arguments are correct, execute it. Otherwise, inform the user that the request is not possible.
"""

prompt = 'Get me the 20 Day Moving Average Stock price for Apple'
print('Prompt:', prompt)

response = client.chat(
    'llama3.1',
    messages=[{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': prompt}],
    tools=[get_current_stock_price_tool, get_20_day_moving_average_tool]
)

print('Response:', response.message)

if response.message.tool_calls:
    for tool in response.message.tool_calls:
        if function_to_call := available_functions.get(tool.function.name):
            print('Calling function:', tool.function.name)
            print('Arguments:', tool.function.arguments)
            if not tool.function.arguments or 'symbol' not in tool.function.arguments or not tool.function.arguments['symbol']:
                print('Error: Missing or empty argument for stock symbol.')
            else:
                function_output = function_to_call(**tool.function.arguments)
                print('Function output:', function_output)
        else:
            print('Function', tool.function.name, 'not found')