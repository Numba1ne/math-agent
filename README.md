# Math Agent

A conversational AI math assistant powered by LangChain and LangGraph, using Meta's Llama 3 model via OpenRouter.

## Features

- **Interactive Chat Interface**: Conversational interface for solving math problems
- **Multiple Math Operations**:
  - Basic arithmetic (addition, subtraction, multiplication, division)
  - Power and exponent calculations
  - Square root calculations
- **Intelligent Tool Selection**: The agent automatically selects the appropriate tool based on your question
- **Error Handling**: Built-in validation for operations like division by zero and negative square roots

## Prerequisites

- Python 3.13 or higher
- OpenRouter API key

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

3. Create a `.env` file in the project root and add your OpenRouter API key:
```
OPENROUTER_API_KEY=your_api_key_here
```

## Usage

Run the agent:
```bash
python main.py
```

Example interactions:
```
You: What is 25 + 17?
Assistant: The sum of 25 and 17 is 42

You: Calculate 5 to the power of 3
Assistant: 5 raised to the power of 3 is 125

You: What's the square root of 144?
Assistant: The square root of 144 is 12.0

You: Divide 100 by 4
Assistant: The division of 100 by 4 is 25.0
```

Type `quit` to exit the application.

## Project Structure

```
math-agent/
├── main.py           # Main application file with agent and tools
├── pyproject.toml    # Project dependencies and configuration
├── .env              # Environment variables (not tracked in git)
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

## Technologies Used

- [LangChain](https://python.langchain.com/) - Framework for building LLM applications
- [LangGraph](https://langchain-ai.github.io/langgraph/) - Library for building stateful, multi-actor applications
- [OpenRouter](https://openrouter.ai/) - Unified API for multiple LLM providers
- [Llama 3](https://ai.meta.com/llama/) - Meta's open-source language model

## License

MIT License
