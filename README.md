# gitcommit
Tooling to create smart git commit messages.


## Getting started

Checkout the repository and create a virtual environment a `venv` folder.
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

## Motivation
Finding the right commit message is hard. Maybe it's even tempting to ignore them and add a placeholder instead. Every git user did the `git commit -m '.'` at some point in their career.

### What it does
`igit commit` takes information from your issue tracker, the git repository and the staged code. Those are used to render a smart commit message template, helping the developer to fill them with meaningful and explaining content.

### How we built it
We built igit as a python package with focus on extensibility of information sources, e.g. the issue tracker or language support. To interface with git, we used `pygit2`. Template rendering is done via `jinja2`.

Information are gathered in dedicated modules and rendered with a template that can be configured for different git repositories similar to a `.gitignore`file.

### Challenges we ran into
- missing or incomplete documentation for a package
- working on a subset of files with multiple people (happy merging!)

### Accomplishments that we're proud of
- working command line interface
- structured repository

### What we learned
We learned that collaborative work, given only a short amount of time, is challenging. But working in a small (local) team makes prioritizing issues and solving problems as they arise a lot easier. Someone with an idea is around to help.

### What's next for igit commit
The next steps involve building a `igit` command line interface, supporting:
- other programming languages
- different issue trackers (e.g. GitHub, Atlassian Bitbucket)
- more subcommands, helping the developers with changelog creation or merge request processing

