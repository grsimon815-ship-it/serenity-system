# Contributing to PolyglotForge Studio

We love your input! We want to make contributing to PolyglotForge as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new language paradigms or memory scenarios
- Adding new architecture patterns

## Development Process

1. Fork the repo and create your branch from `main`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the unit test suite:
   ```bash
   python -m unittest discover tests
   ```
4. If you've added new paradigms or patterns, add corresponding test cases in `tests/test_core.py`.
5. Ensure your code passes all checks before opening a Pull Request.

## Coding Conventions

- Follow PEP 8 style guidelines for Python.
- Keep UI components decoupled from data definitions in `core/`.
- Maintain dark-mode cyber styling consistency in `ui/theme.py`.
