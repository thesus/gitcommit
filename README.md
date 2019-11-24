# gitcommit
Tooling to create smart git commit messages.


## Getting started

Checkout repository and create a virtual environment a `venv` folder.
```sh
python3 -m venv venv
```

Everytime you interact with the project, activate your virtual environment.
```sh
source venv/bin/activate
```

Install development requirements  with:
```sh
pip install -r requirements/development.txt
```

Take a look at the cli at `src/main.py`

In order to run it, use:
```sh
python -m gitcommit
```

## Tests
To run the tests use pytest in the repo-root.

```sh
pytest --cov gitcommit
```

This runs all tests and prints the current coverage to the terminal.

## Building
To build and install the programm run `pip install -e .`

You can access it via `igit`
