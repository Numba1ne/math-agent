import os
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()


@tool
def calculator(a: float, b: float, operation: str = "add") -> str:
    """Useful for performing basic arithmetic calculations with numbers.

    Args:
        a: First number
        b: Second number
        operation: The operation to perform (add, subtract, multiply, divide)
    """
    print("Calculator tool has been called.")

    if operation == "add":
        result = a + b
        return f"The sum of {a} and {b} is {result}"
    elif operation == "subtract":
        result = a - b
        return f"The difference of {a} and {b} is {result}"
    elif operation == "multiply":
        result = a * b
        return f"The product of {a} and {b} is {result}"
    elif operation == "divide":
        if b == 0:
            return "Error: Cannot divide by zero"
        result = a / b
        return f"The division of {a} by {b} is {result}"
    else:
        return f"Unknown operation: {operation}"


@tool
def power(base: float, exponent: float) -> str:
    """Useful for calculating powers and exponents.

    Args:
        base: The base number
        exponent: The exponent/power
    """
    print("Power tool has been called.")
    result = base**exponent
    return f"{base} raised to the power of {exponent} is {result}"


@tool
def square_root(number: float) -> str:
    """Useful for calculating the square root of a number.

    Args:
        number: The number to find the square root of
    """
    print("Square root tool has been called.")
    if number < 0:
        return "Error: Cannot calculate square root of a negative number"
    result = number**0.5
    return f"The square root of {number} is {result}"


def main():
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_api_key:
        raise ValueError("OPENROUTER_API_KEY not found. Check your .env file.")

    # OpenRouter works with the OpenAI-compatible endpoint
    model = ChatOpenAI(
        api_key=openrouter_api_key,
        base_url="https://openrouter.ai/api/v1",
        model="meta-llama/llama-3-8b-instruct",
        temperature=0,
    )

    tools = [calculator, power, square_root]
    agent_executor = create_react_agent(model, tools)

    print("Welcome! I'm your Math AI assistant. Type 'quit' to exit.")
    print("You can ask me to perform calculations like:")
    print("  - Add, subtract, multiply, or divide numbers")
    print("  - Calculate powers and square roots")
    print("  - Solve math problems")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        if not user_input:
            continue

        print("\nAssistant: ", end="")
        try:
            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=user_input)]}
            ):
                if "agent" in chunk and "messages" in chunk["agent"]:
                    for message in chunk["agent"]["messages"]:
                        print(message.content, end="")
            print()
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again with a different question.")


if __name__ == "__main__":
    main()
