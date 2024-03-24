# Graduation-Project
Recommandation System and GAI App for Co-Living of Young and Ederly


### Setting Up a Virtual Environment

Before running any Python-based frameworks, it's recommended to set up a virtual environment. This isolates your project dependencies and ensures that your development environment remains clean and manageable.

```bash
# Create a virtual environment
python3 -m venv myvenv

# Activate the virtual environment
source myvenv/bin/activate
```


### FastAPI

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. To set up FastAPI:

```bash
# Install FastAPI with all optional dependencies
pip install "fastapi[all]"

# Start the FastAPI server with live reloading
uvicorn main:app --reload
```