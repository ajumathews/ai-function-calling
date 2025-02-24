import oracledb
import ollama
from typing import Dict, Callable

def query_products(price: float, stock_quantity: int) -> list:
    connection = oracledb.connect(user='ECOM', password='ECOM', dsn='localhost:1521/xe')
    cursor = connection.cursor()
    
    sql = """
    SELECT product_id, product_name, product_description, price, stock_quantity 
    FROM ECOM.products
    WHERE price <= :price AND stock_quantity >= :stock_quantity
    """
    
    cursor.execute(sql, {'price': price, 'stock_quantity': stock_quantity})
    
    # Fetch the results
    products = cursor.fetchall()
    
    # Clean up and close the connection
    cursor.close()
    connection.close()
    
    # Return the results as a list of dictionaries for easier interpretation
    product_list = []
    for row in products:
        product_list.append({
            "product_id": row[0],
            "product_name": row[1],
            "product_description": row[2],
            "price": row[3],
            "stock_quantity": row[4],
        })
    
    return product_list

# Define the tool for calling the above function via Ollama
query_products_tool = {
    'type': 'function',
    'function': {
        'name': 'query_products',
        'description': 'Query the products table based on price and stock quantity',
        'parameters': {
            'type': 'object',
            'required': ['price', 'stock_quantity'],
            'properties': {
                'price': {'type': 'number', 'description': 'Maximum price of products'},
                'stock_quantity': {'type': 'integer', 'description': 'Minimum stock quantity of products'},
            },
        },
    },
}

# Define available functions in the system
available_functions: Dict[str, Callable] = {
    'query_products': query_products,
}

# Example prompt for querying products with price and stock quantity filters
prompt = 'Find all laptops with a price less than $1000 and at least 10 in stock'
print('Prompt:', prompt)

# Simulate the response from Ollama using the chat system
response = ollama.chat(
    'llama3.2',
    messages=[{'role': 'user', 'content': prompt}],
    tools=[query_products_tool],
)

# Check for any function calls in the response
if response.message.tool_calls:
    for tool in response.message.tool_calls:
        if function_to_call := available_functions.get(tool.function.name):
            print('Calling function:', tool.function.name)
            print('Arguments:', tool.function.arguments)
            # Call the function with the arguments from the tool
            result = function_to_call(**tool.function.arguments)
            print('Function output:', result)
        else:
            print('Function', tool.function.name, 'not found')
