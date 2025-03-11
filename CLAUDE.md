# CLAUDE.md - JoTa AI Django Project Guidelines

## Build & Run Commands
- Setup: `pip install -r requirements.txt`
- Run server: `python manage.py runserver`
- Run with specific port: `python manage.py runserver 8080`
- Create migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`
- Django shell: `python manage.py shell`
- Deploy with: `gunicorn project.wsgi`

## Testing
- Run all tests: `python manage.py test`
- Single test file: `python manage.py test project.tests.test_filters`
- Single test: `python manage.py test project.tests.test_filters.TestComicEffect`

## Code Style Guidelines
- Follow PEP 8 conventions for Python code
- Class names: CamelCase (e.g., `FilterView`)
- Functions/variables: snake_case (e.g., `comic_effect`)
- Import order: stdlib → third-party → local modules
- Docstrings: Use triple quotes with Parameters and Returns sections
- Error handling: Use specific exceptions with descriptive messages
- Type hints: Add to new code (not yet implemented in codebase)