import os
import math
import statistics
from pathlib import Path
from typing import List, Optional
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import sympy as sp

load_dotenv()

# Load system prompt
PROMPTS_DIR = Path(__file__).parent / "prompts"
SYSTEM_PROMPT_PATH = PROMPTS_DIR / "system_prompt.txt"

def load_system_prompt() -> str:
    """Load the system prompt from the prompts folder."""
    if SYSTEM_PROMPT_PATH.exists():
        with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    else:
        # Fallback prompt if file doesn't exist
        return "You are a specialized Math AI Assistant focused solely on mathematical calculations and problem-solving."
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


# ========== ALGEBRA TOOLS ==========

@tool
def solve_linear_equation(equation: str) -> str:
    """Solve a linear equation in one variable. Equation should be in the form 'ax + b = c' or similar.
    
    Args:
        equation: The equation to solve as a string, e.g., '2*x + 5 = 13' or '3*x - 7 = 2'
    """
    try:
        # Parse and solve the equation
        x = sp.Symbol('x')
        if '=' in equation:
            parts = equation.split('=')
            left = sp.sympify(parts[0].strip())
            right = sp.sympify(parts[1].strip())
            solution = sp.solve(left - right, x)
        else:
            # If no equals sign, try to solve the expression = 0
            expr = sp.sympify(equation)
            solution = sp.solve(expr, x)
        
        if solution:
            return f"Solution: x = {solution[0]}"
        else:
            return "No solution found or equation is not linear."
    except Exception as e:
        return f"Error solving equation: {str(e)}. Please provide equation in format like '2*x + 5 = 13'"


@tool
def solve_quadratic_equation(a: float, b: float, c: float) -> str:
    """Solve a quadratic equation ax² + bx + c = 0 using the quadratic formula.
    
    Args:
        a: Coefficient of x²
        b: Coefficient of x
        c: Constant term
    """
    if a == 0:
        return "Error: This is not a quadratic equation (a cannot be 0)"
    
    discriminant = b**2 - 4*a*c
    
    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        return f"Two real solutions: x₁ = {x1}, x₂ = {x2}"
    elif discriminant == 0:
        x = -b / (2*a)
        return f"One real solution (repeated root): x = {x}"
    else:
        real_part = -b / (2*a)
        imag_part = math.sqrt(-discriminant) / (2*a)
        return f"Two complex solutions: x₁ = {real_part} + {imag_part}i, x₂ = {real_part} - {imag_part}i"


@tool
def factor_expression(expression: str) -> str:
    """Factor a mathematical expression.
    
    Args:
        expression: The expression to factor, e.g., 'x^2 + 5*x + 6' or 'x^2 - 9'
    """
    try:
        x = sp.Symbol('x')
        expr = sp.sympify(expression)
        factored = sp.factor(expr)
        return f"Factored form: {factored}"
    except Exception as e:
        return f"Error factoring expression: {str(e)}"


@tool
def expand_expression(expression: str) -> str:
    """Expand a mathematical expression.
    
    Args:
        expression: The expression to expand, e.g., '(x + 2)*(x + 3)' or '(x + 1)^2'
    """
    try:
        x = sp.Symbol('x')
        expr = sp.sympify(expression)
        expanded = sp.expand(expr)
        return f"Expanded form: {expanded}"
    except Exception as e:
        return f"Error expanding expression: {str(e)}"


# ========== GEOMETRY TOOLS ==========

@tool
def area_rectangle(length: float, width: float) -> str:
    """Calculate the area of a rectangle.
    
    Args:
        length: Length of the rectangle
        width: Width of the rectangle
    """
    area = length * width
    return f"Area of rectangle: {area} square units"


@tool
def area_triangle(base: float, height: float) -> str:
    """Calculate the area of a triangle.
    
    Args:
        base: Base length of the triangle
        height: Height of the triangle
    """
    area = 0.5 * base * height
    return f"Area of triangle: {area} square units"


@tool
def area_circle(radius: float) -> str:
    """Calculate the area of a circle.
    
    Args:
        radius: Radius of the circle
    """
    area = math.pi * radius**2
    return f"Area of circle: {area:.4f} square units (π × r² = π × {radius}²)"


@tool
def circumference_circle(radius: float) -> str:
    """Calculate the circumference of a circle.
    
    Args:
        radius: Radius of the circle
    """
    circumference = 2 * math.pi * radius
    return f"Circumference of circle: {circumference:.4f} units (2πr = 2π × {radius})"


@tool
def volume_cylinder(radius: float, height: float) -> str:
    """Calculate the volume of a cylinder.
    
    Args:
        radius: Radius of the base
        height: Height of the cylinder
    """
    volume = math.pi * radius**2 * height
    return f"Volume of cylinder: {volume:.4f} cubic units (πr²h = π × {radius}² × {height})"


@tool
def volume_sphere(radius: float) -> str:
    """Calculate the volume of a sphere.
    
    Args:
        radius: Radius of the sphere
    """
    volume = (4/3) * math.pi * radius**3
    return f"Volume of sphere: {volume:.4f} cubic units ((4/3)πr³ = (4/3)π × {radius}³)"


@tool
def volume_cone(radius: float, height: float) -> str:
    """Calculate the volume of a cone.
    
    Args:
        radius: Radius of the base
        height: Height of the cone
    """
    volume = (1/3) * math.pi * radius**2 * height
    return f"Volume of cone: {volume:.4f} cubic units ((1/3)πr²h = (1/3)π × {radius}² × {height})"


@tool
def pythagorean_theorem(a: Optional[float] = None, b: Optional[float] = None, c: Optional[float] = None) -> str:
    """Calculate the missing side of a right triangle using the Pythagorean theorem (a² + b² = c²).
    Provide any two sides to find the third.
    
    Args:
        a: Length of side a
        b: Length of side b
        c: Length of hypotenuse c
    """
    if a is not None and b is not None and c is None:
        c = math.sqrt(a**2 + b**2)
        return f"Hypotenuse c = {c:.4f} (√(a² + b²) = √({a}² + {b}²))"
    elif a is not None and c is not None and b is None:
        b = math.sqrt(c**2 - a**2)
        return f"Side b = {b:.4f} (√(c² - a²) = √({c}² - {a}²))"
    elif b is not None and c is not None and a is None:
        a = math.sqrt(c**2 - b**2)
        return f"Side a = {a:.4f} (√(c² - b²) = √({c}² - {b}²))"
    else:
        return "Error: Please provide exactly two sides to find the third"


# ========== TRIGONOMETRY TOOLS ==========

@tool
def sin(angle_degrees: float) -> str:
    """Calculate the sine of an angle in degrees.
    
    Args:
        angle_degrees: Angle in degrees
    """
    result = math.sin(math.radians(angle_degrees))
    return f"sin({angle_degrees}°) = {result:.6f}"


@tool
def cos(angle_degrees: float) -> str:
    """Calculate the cosine of an angle in degrees.
    
    Args:
        angle_degrees: Angle in degrees
    """
    result = math.cos(math.radians(angle_degrees))
    return f"cos({angle_degrees}°) = {result:.6f}"


@tool
def tan(angle_degrees: float) -> str:
    """Calculate the tangent of an angle in degrees.
    
    Args:
        angle_degrees: Angle in degrees
    """
    result = math.tan(math.radians(angle_degrees))
    return f"tan({angle_degrees}°) = {result:.6f}"


@tool
def arcsin(value: float) -> str:
    """Calculate the arcsine (inverse sine) in degrees.
    
    Args:
        value: Value between -1 and 1
    """
    if -1 <= value <= 1:
        result = math.degrees(math.asin(value))
        return f"arcsin({value}) = {result:.4f}°"
    else:
        return "Error: Value must be between -1 and 1"


@tool
def arccos(value: float) -> str:
    """Calculate the arccosine (inverse cosine) in degrees.
    
    Args:
        value: Value between -1 and 1
    """
    if -1 <= value <= 1:
        result = math.degrees(math.acos(value))
        return f"arccos({value}) = {result:.4f}°"
    else:
        return "Error: Value must be between -1 and 1"


@tool
def arctan(value: float) -> str:
    """Calculate the arctangent (inverse tangent) in degrees.
    
    Args:
        value: Any real number
    """
    result = math.degrees(math.atan(value))
    return f"arctan({value}) = {result:.4f}°"


# ========== LOGARITHMS AND EXPONENTIALS ==========

@tool
def logarithm(base: float, number: float) -> str:
    """Calculate the logarithm of a number with a given base.
    
    Args:
        base: Base of the logarithm
        number: Number to take the logarithm of
    """
    if base <= 0 or base == 1:
        return "Error: Base must be positive and not equal to 1"
    if number <= 0:
        return "Error: Number must be positive"
    result = math.log(number, base)
    return f"log_{base}({number}) = {result:.6f}"


@tool
def natural_log(number: float) -> str:
    """Calculate the natural logarithm (base e) of a number.
    
    Args:
        number: Number to take the natural logarithm of
    """
    if number <= 0:
        return "Error: Number must be positive"
    result = math.log(number)
    return f"ln({number}) = {result:.6f}"


@tool
def log10(number: float) -> str:
    """Calculate the base-10 logarithm of a number.
    
    Args:
        number: Number to take the base-10 logarithm of
    """
    if number <= 0:
        return "Error: Number must be positive"
    result = math.log10(number)
    return f"log₁₀({number}) = {result:.6f}"


@tool
def exponential(power: float) -> str:
    """Calculate e raised to a power.
    
    Args:
        power: The exponent
    """
    result = math.exp(power)
    return f"e^{power} = {result:.6f}"


# ========== STATISTICS TOOLS ==========

@tool
def mean(numbers: List[float]) -> str:
    """Calculate the mean (average) of a list of numbers.
    
    Args:
        numbers: List of numbers
    """
    if not numbers:
        return "Error: List cannot be empty"
    result = statistics.mean(numbers)
    return f"Mean: {result:.4f}"


@tool
def median(numbers: List[float]) -> str:
    """Calculate the median of a list of numbers.
    
    Args:
        numbers: List of numbers
    """
    if not numbers:
        return "Error: List cannot be empty"
    result = statistics.median(numbers)
    return f"Median: {result:.4f}"


@tool
def mode(numbers: List[float]) -> str:
    """Calculate the mode (most frequent value) of a list of numbers.
    
    Args:
        numbers: List of numbers
    """
    if not numbers:
        return "Error: List cannot be empty"
    try:
        result = statistics.mode(numbers)
        return f"Mode: {result}"
    except statistics.StatisticsError:
        return "No unique mode found (all values appear equally often)"


@tool
def standard_deviation(numbers: List[float]) -> str:
    """Calculate the standard deviation of a list of numbers.
    
    Args:
        numbers: List of numbers
    """
    if not numbers or len(numbers) < 2:
        return "Error: Need at least 2 numbers"
    result = statistics.stdev(numbers)
    return f"Standard deviation: {result:.4f}"


@tool
def variance(numbers: List[float]) -> str:
    """Calculate the variance of a list of numbers.
    
    Args:
        numbers: List of numbers
    """
    if not numbers or len(numbers) < 2:
        return "Error: Need at least 2 numbers"
    result = statistics.variance(numbers)
    return f"Variance: {result:.4f}"


# ========== SEQUENCES AND SERIES ==========

@tool
def arithmetic_sequence_nth_term(first_term: float, common_difference: float, n: int) -> str:
    """Find the nth term of an arithmetic sequence: aₙ = a₁ + (n-1)d
    
    Args:
        first_term: First term (a₁)
        common_difference: Common difference (d)
        n: Term number
    """
    nth_term = first_term + (n - 1) * common_difference
    return f"Term {n} (aₙ): {nth_term} (a₁ + (n-1)d = {first_term} + ({n}-1) × {common_difference})"


@tool
def arithmetic_sequence_sum(first_term: float, last_term: float, n: int) -> str:
    """Find the sum of the first n terms of an arithmetic sequence: Sₙ = n(a₁ + aₙ)/2
    
    Args:
        first_term: First term (a₁)
        last_term: Last term (aₙ)
        n: Number of terms
    """
    sum_result = n * (first_term + last_term) / 2
    return f"Sum of first {n} terms: {sum_result} (n(a₁ + aₙ)/2 = {n}({first_term} + {last_term})/2)"


@tool
def geometric_sequence_nth_term(first_term: float, common_ratio: float, n: int) -> str:
    """Find the nth term of a geometric sequence: aₙ = a₁ × r^(n-1)
    
    Args:
        first_term: First term (a₁)
        common_ratio: Common ratio (r)
        n: Term number
    """
    nth_term = first_term * (common_ratio ** (n - 1))
    return f"Term {n} (aₙ): {nth_term} (a₁ × r^(n-1) = {first_term} × {common_ratio}^({n}-1))"


@tool
def geometric_sequence_sum(first_term: float, common_ratio: float, n: int) -> str:
    """Find the sum of the first n terms of a geometric sequence: Sₙ = a₁(1-rⁿ)/(1-r)
    
    Args:
        first_term: First term (a₁)
        common_ratio: Common ratio (r)
        n: Number of terms
    """
    if common_ratio == 1:
        sum_result = n * first_term
        return f"Sum of first {n} terms: {sum_result} (when r=1, Sₙ = n × a₁)"
    sum_result = first_term * (1 - common_ratio**n) / (1 - common_ratio)
    return f"Sum of first {n} terms: {sum_result:.4f} (a₁(1-rⁿ)/(1-r) = {first_term}(1-{common_ratio}^{n})/(1-{common_ratio}))"


# ========== PERCENTAGES AND RATIOS ==========

@tool
def percentage(part: float, whole: float) -> str:
    """Calculate what percentage one number is of another.
    
    Args:
        part: The part
        whole: The whole
    """
    if whole == 0:
        return "Error: Whole cannot be zero"
    result = (part / whole) * 100
    return f"{part} is {result:.2f}% of {whole}"


@tool
def percentage_of(percentage: float, number: float) -> str:
    """Calculate a percentage of a number.
    
    Args:
        percentage: The percentage (e.g., 25 for 25%)
        number: The number
    """
    result = (percentage / 100) * number
    return f"{percentage}% of {number} = {result}"


@tool
def ratio_simplify(a: float, b: float) -> str:
    """Simplify a ratio to its simplest form.
    
    Args:
        a: First number
        b: Second number
    """
    if b == 0:
        return "Error: Second number cannot be zero"
    gcd = math.gcd(int(a), int(b)) if a == int(a) and b == int(b) else 1
    simplified_a = a / gcd if gcd > 1 else a
    simplified_b = b / gcd if gcd > 1 else b
    return f"Ratio {a}:{b} simplified = {simplified_a}:{simplified_b}"


def get_all_tools():
    """Get all math tools for the agent."""
    return [
        # Basic arithmetic
        calculator, power, square_root,
        # Algebra
        solve_linear_equation, solve_quadratic_equation, factor_expression, expand_expression,
        # Geometry
        area_rectangle, area_triangle, area_circle, circumference_circle,
        volume_cylinder, volume_sphere, volume_cone, pythagorean_theorem,
        # Trigonometry
        sin, cos, tan, arcsin, arccos, arctan,
        # Logarithms
        logarithm, natural_log, log10, exponential,
        # Statistics
        mean, median, mode, standard_deviation, variance,
        # Sequences
        arithmetic_sequence_nth_term, arithmetic_sequence_sum,
        geometric_sequence_nth_term, geometric_sequence_sum,
        # Percentages and ratios
        percentage, percentage_of, ratio_simplify,
    ]


def initialize_agent():
    """Initialize the math agent with all tools. Returns (agent_executor, system_message, api_status)."""
    # Try OpenAI API key first, fallback to OpenRouter
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    
    if openai_api_key:
        # Use direct OpenAI API
        model = ChatOpenAI(
            api_key=openai_api_key,
            model="gpt-4o-mini",  # You can change to "gpt-4o" or "gpt-3.5-turbo"
            temperature=0,
        )
        api_status = "Using direct OpenAI API"
    elif openrouter_api_key:
        # Fallback to OpenRouter
        model = ChatOpenAI(
            api_key=openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
            model="openai/gpt-4o-mini",  # You can change to "openai/gpt-4" or "openai/gpt-3.5-turbo"
            temperature=0,
        )
        api_status = "Using OpenRouter API (fallback)"
    else:
        raise ValueError(
            "Neither OPENAI_API_KEY nor OPENROUTER_API_KEY found. "
            "Please add one of them to your .env file."
        )

    # Comprehensive math tools for secondary school
    tools = get_all_tools()
    
    agent_executor = create_react_agent(model, tools)
    
    # Load system prompt once at startup
    system_prompt = load_system_prompt()
    system_message = SystemMessage(content=system_prompt)
    
    return agent_executor, system_message, api_status


def main():
    agent_executor, system_message, api_status = initialize_agent()
    print(api_status)

    print("Welcome! I'm your comprehensive Math AI assistant for secondary school exam preparation.")
    print("I can help you with:")
    print("  📐 Algebra: Solving equations, factoring, expanding expressions")
    print("  📏 Geometry: Areas, volumes, perimeters, Pythagorean theorem")
    print("  📊 Trigonometry: sin, cos, tan, and their inverses")
    print("  📈 Statistics: Mean, median, mode, standard deviation, variance")
    print("  🔢 Sequences: Arithmetic and geometric sequences")
    print("  📉 Logarithms and exponentials")
    print("  ➕ Basic arithmetic, percentages, and ratios")
    print("\nType 'quit' to exit.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        if not user_input:
            continue

        print("\nAssistant: ", end="")
        try:
            # Create messages with system instruction
            messages = [
                system_message,
                HumanMessage(content=user_input)
            ]
            
            for chunk in agent_executor.stream({"messages": messages}):
                if "agent" in chunk and "messages" in chunk["agent"]:
                    for message in chunk["agent"]["messages"]:
                        print(message.content, end="")
            print()
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again with a different question.")


if __name__ == "__main__":
    main()
