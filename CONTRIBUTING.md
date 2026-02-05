# Contributing to OpenPlugin

Thank you for your interest in contributing to OpenPlugin!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/openplugin
cd openplugin
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

## Code Style

We use:
- `black` for code formatting
- `ruff` for linting
- `mypy` for type checking

Run checks:
```bash
black openplugin/
ruff check openplugin/
mypy openplugin/
```

## Adding a New Provider

1. Create a new file in `openplugin/providers/` (e.g., `anthropic_provider.py`)
2. Implement the `LLMProvider` interface
3. Add conversion logic for MCP tools to provider format
4. Export in `openplugin/providers/__init__.py`
5. Add tests
6. Update documentation

## Adding Features

1. Create an issue to discuss the feature
2. Fork the repository
3. Create a feature branch
4. Make your changes
5. Add tests
6. Update documentation
7. Submit a pull request

## Plugin Development

To test your plugin:
1. Place it in the `plugins/` directory
2. Use the example script to test:
```bash
python examples/basic_usage.py
```

## Questions?

Open an issue or start a discussion!
