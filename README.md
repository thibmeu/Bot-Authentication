# Web bot auth Python

![GitHub License](https://img.shields.io/github/license/cloudflareresearch/web-bot-auth)

Implementation of web bot auth in python

## Requirements

* [Python 3.13](https://www.python.org/downloads/)
* [uv](https://docs.astral.sh/uv/getting-started/installation/) - Python package manager

## Development

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

### Lint

This codebase uses [ruff](https://docs.astral.sh/ruff/) and [Black](https://black.readthedocs.io/en/stable/index.html) for linting.

For run a check, use

```shell
uv run ruff check .
uv run black --check .
```

To format the codebase

```shell

uv run ruff format .
uv run black .
```

## Security Considerations

This software has not been audited. Please use at your sole discretion.

## License

This project is under the Apache 2.0 license.

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you shall be Apache 2.0 licensed as above, without any additional terms or conditions.
