# from dotenv import load_dotenv

# load_dotenv()

# import ollama
# from langsmith import traceable

# MAX_ITERATIONS = 10
# MODEL = "qwen3:1.7b"

# # --- Tools (LangChain @tool decorator) ---

# PRODUCT_PRICES = {
#     "laptop": 999.99,
#     "phone": 699.99,
#     "headphones": 149.99,
# }


# @traceable(run_type="tool")
# def get_product_price(product: str) -> float:
#     """Look up the price of a product in the catalog"""
#     print(f"Looking up price for product: {product}")
#     prices = {"laptop": 999.99, "phone": 699.99, "keyboard": 149.99}
#     return prices.get(product, 0)  # Return -1.0 if product not found



# @traceable(run_type="tool")
# def apply_discount(price: float, discount_tier: str) -> float:
#     """Apply a discount to a price and return final price
#     Available tier : bronze, silver, gold"""
#     print(f"Applying discount: {discount_tier} to price: {price}")
#     discount_percentages = {"bronze": 0.05, "silver": 0.10, "gold": 0.15}
#     discount = discount_percentages.get(discount_tier, 0)
#     return round(price * (1 - discount),2)


# tools_for_llm = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_product_price",
#             "description": "Look up the price of a product in the catalog",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "product": {"type": "string", "description": "The name of the product to look up"}
#                 },
#                 "required": ["product"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "apply_discount",
#             "description": "Apply a discount to a price and return final price",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "price": {"type": "number", "description": "The original price"},
#                     "discount_tier": {"type": "string", "description": "The discount tier to apply"}
#                 },
#                 "required": ["price", "discount_tier"]
#             }
#         }
#     }
# ]

# # --- Helper:traced Ollama call ---
# @traceable(name="Ollama Chat,run_type="llm")
# def ollama_chat_traced(messages):
#     return ollama.chat(
#         model=MODEL,
#         messages=messages,
#         tools=tools_for_llm,
#         temperature=0
#     )


# # --- Agent Loop ---
# @traceable(name="LangCHain Agent Loop")
# def run_agent(question: str):
   
#     tools_dict = {
#         "get_product_price": get_product_price,
#         "apply_discount": apply_discount
#     }
   
#     print(f"Question: {question}")
#     print("=" * 605)

#     messages = [
#        {"role": "system", 
#         "content": ( 
#                         "You are a helpful shopping assistant. You have access to the Product catalog tools "
#                        "and a discount tool."
#                        "STRICT RULES - you must follow these exactly:"
#                        "1. NEVER guess or assume any product price."
#                        "YOU MUST call get_product_price to get the price of a product."
#                        "2. Only call apply_discount after you have obtained the product price from get_product_price."
#                        "Pass the exact price returned by get_product_price to apply_discount - do NOT pass a made-up number."
#                        "3. NEVER calucalte discounts yourself using match. Always use the apply_discount tool to calculate the final price."
#                        "4. If the user does not specity a discunt tier, ask them which tier to use - do NOT asume one."
#                        "5. If product does not find in catalog, return message to user that Product is not eligible for discount.")},
#         {"role": "user", "content": question}
#     ]

#     #-------Agent Loop-------
    
#     for iteration in range(1, MAX_ITERATIONS + 1):
#         print(f"Iteration {iteration} of {MAX_ITERATIONS}")

#         response = ollama_chat_traced(messages=messages)
#         ai_message = response.message

#         tool_calls = ai_message.tool_calls

#         # If no tool calls, this is the final answer
#         if not tool_calls:
#             print(f"Final Answer: {ai_message.content}")
#             return ai_message.content

#         #Process only the FIRST tool call - force one tool per iteration
#         tool_call = tool_calls[0]
#         tool_name = tool_call.get("name")
#         tool_args = tool_call.get("args", {})
#         tool_call_id = tool_call.get("id")

#         print(f"Tool Selected: {tool_name} with args: {tool_args}")
#         tool_to_use = tools_dict.get(tool_name)

#         if tool_to_use is None:
#             raise ValueError(f"Tool {tool_name} not found in tools_dict")

#         observation = tool_to_use.invoke(tool_args)
#         print(f"Observation from tool {tool_name}: {observation}")
#         messages.append(ai_message)
#         messages.append(ToolMessage(content=str(observation), tool_call_id=tool_call_id))

#     print("Max iterations reached without a final answer.")
#     return None

# if __name__ == "__main__":
#     question = "What is the price of a bike with a gold discount?"
#     result = run_agent(question)
#     print(f"Result: {result}")