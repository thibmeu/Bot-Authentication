# Web bot auth Python

Implementation of web bot auth in python

## Requirements

* [Python 3.13](https://www.python.org/downloads/)
* [uv](https://docs.astral.sh/uv/getting-started/installation/) - Python package manager

## Devevlopment

To build web-bot-auth package

```shell
python3 -m venv .venv
source .venv/bin/activate

uv build
uv pip install -e .
```

Examples are in the `examples` folder.

```shell
uv run examples/crawl4ai-hook/main.py
```
