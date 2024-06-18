# where-my-money

- **autor:** Rene Hlavova rene.hlavova@gmail.com
- **created:** 2023-03-08

## Description

### What it is used for

### What the code does

The `where_my_money` package does:

1. text
2. text
3. text

## Requirements

See [`pyproject.toml`](./pyproject.toml)

## How to use it

### Installation

Install this project using `poetry`.

```console
poetry install
```

### Commands

- `poe isort`
  - sort imports using `isort`
- `poe isort-check`
  - check imports are sorted using `isort`
- `poe black`
  - format Python files using `black`
- `poe black-check`
  - check Python formatting using `black`
- `poe mypy`
  - use `mypy` to static check Python types
- `poe pylint`
  - use `pylint` to lint your Python files
- `poe format`
  - run `isort` and `black` in succession
- `poe lint`
  - run `isort-check`, `black-check`, `pylint` and `mypy` in succession
- `poe test`
  - run `pytest` and generate coverage report
- `poe coverage`
  - display coverage from last test run
- `poe tox`
  - run all tests and build against all supported Python versions
- `poe docs`
  - build docs using docstrings and `pdoc3`
- `poe docker`
  - build project using `docker`
  - target image is `bizztreat/where_my_money`
- `poe run`
  - run the project

## TODO
