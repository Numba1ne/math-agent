# Math Agent

A comprehensive conversational AI math assistant designed for secondary school students preparing for national exams. Powered by LangChain and LangGraph, with support for OpenAI and OpenRouter APIs.

## Features

- **Interactive Chat Interface**: Conversational interface for solving math problems
- **Comprehensive Math Coverage**: Supports all major secondary school mathematics topics
- **Intelligent Tool Selection**: The agent automatically selects the appropriate tool based on your question
- **Step-by-Step Solutions**: Provides clear explanations and shows work for exam preparation
- **Error Handling**: Built-in validation for mathematical operations

## Math Topics Covered

### 📐 Algebra
- Solving linear equations
- Solving quadratic equations (with quadratic formula)
- Factoring algebraic expressions
- Expanding algebraic expressions

### 📏 Geometry
- **Areas**: Rectangle, triangle, circle
- **Volumes**: Cylinder, sphere, cone
- **Perimeters & Circumferences**: Circle circumference
- **Pythagorean Theorem**: Finding missing sides of right triangles

### 📊 Trigonometry
- Sine, cosine, tangent functions (in degrees)
- Inverse trigonometric functions (arcsin, arccos, arctan)

### 📈 Statistics
- Mean (average)
- Median
- Mode
- Standard deviation
- Variance

### 🔢 Sequences and Series
- **Arithmetic Sequences**: Finding nth term and sum
- **Geometric Sequences**: Finding nth term and sum

### 📉 Logarithms and Exponentials
- Logarithms with any base
- Natural logarithm (ln)
- Base-10 logarithm (log₁₀)
- Exponential functions (e^x)

### ➕ Basic Operations
- Arithmetic (addition, subtraction, multiplication, division)
- Powers and exponents
- Square roots
- Percentages
- Ratio simplification

## Prerequisites

- Python 3.13 or higher
- OpenAI API key OR OpenRouter API key

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd math-agent
```

2. Install dependencies:
```bash
pip install -e .
```

3. Create a `.env` file in the project root and add your API key:
```
# Option 1: Direct OpenAI API (recommended)
OPENAI_API_KEY=your_openai_api_key_here

# Option 2: OpenRouter API (fallback)
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

The agent will automatically use OpenAI if available, otherwise fall back to OpenRouter.

## Usage

Run the agent:
```bash
python main.py
```

### Example Interactions

**Basic Arithmetic:**
```
You: What is 25 + 17?
Assistant: The sum of 25 and 17 is 42

You: Calculate 5 to the power of 3
Assistant: 5 raised to the power of 3 is 125
```

**Algebra:**
```
You: Solve 2*x + 5 = 13
Assistant: Solution: x = 4

You: Solve the quadratic equation with a=1, b=-5, c=6
Assistant: Two real solutions: x₁ = 3.0, x₂ = 2.0
```

**Geometry:**
```
You: Find the area of a circle with radius 5
Assistant: Area of circle: 78.5398 square units (π × r² = π × 5²)

You: Calculate the volume of a cylinder with radius 3 and height 10
Assistant: Volume of cylinder: 282.7433 cubic units
```

**Trigonometry:**
```
You: What is sin(30)?
Assistant: sin(30°) = 0.500000

You: Find arccos(0.5)
Assistant: arccos(0.5) = 60.0000°
```

**Statistics:**
```
You: Find the mean of [10, 20, 30, 40, 50]
Assistant: Mean: 30.0000
```

**Sequences:**
```
You: Find the 10th term of an arithmetic sequence with first term 5 and common difference 3
Assistant: Term 10 (aₙ): 32.0
```

Type `quit` to exit the application.

## Project Structure

```
math-agent/
├── main.py              # Main application file with agent and comprehensive math tools
├── prompts/
│   └── system_prompt.txt # System prompt for focused math assistance
├── pyproject.toml        # Project dependencies and configuration
├── .env                 # Environment variables (not tracked in git)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Technologies Used

- [LangChain](https://python.langchain.com/) - Framework for building LLM applications
- [LangGraph](https://langchain-ai.github.io/langgraph/) - Library for building stateful, multi-actor applications
- [SymPy](https://www.sympy.org/) - Python library for symbolic mathematics
- [OpenAI](https://openai.com/) - AI model provider (primary)
- [OpenRouter](https://openrouter.ai/) - Unified API for multiple LLM providers (fallback)

## Key Features for Exam Preparation

- **Comprehensive Coverage**: All major secondary school math topics
- **Step-by-Step Solutions**: Clear explanations to help understand problem-solving methods
- **Formula References**: Shows relevant formulas in responses
- **Error Handling**: Graceful handling of invalid inputs with clear error messages
- **Exam-Focused**: Structured responses to help with exam-style problems

## License

MIT License
