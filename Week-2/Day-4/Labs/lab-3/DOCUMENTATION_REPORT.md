# Lab 3 — Documentation & Type Hints Report

## Improvements made

- **Type hints**: clarified inputs/outputs (`price: float`, `customer_type: str`, `is_festival: bool`, return `float`).
- **Docstring (Google-style)**: documented arguments, returns, and raised exceptions.
- **Inline comments**: explained non-obvious business intent (premium vs regular discount logic).
- **Error handling**:
  - reject negative prices
  - reject empty/invalid `customer_type`
  - enforce `is_festival` is boolean

## Why this helps

- Makes the business logic easier to understand for new developers.
- Prevents silent bugs from bad inputs.
- Enables static analysis (mypy/IDE tooling) and consistent code quality.

