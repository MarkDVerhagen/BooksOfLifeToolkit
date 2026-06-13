# Contributing to BOLT

Thanks for your interest in improving the Books of Life Toolkit. Contributions of
all kinds are welcome: bug reports, documentation, new data-source instantiators,
and new recipes.

## Development setup

```bash
git clone https://github.com/MarkDVerhagen/BooksOfLifeToolkit.git
cd BooksOfLifeToolkit
python3.12 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"      # core deps + pytest
```

Run the test suite before opening a pull request:

```bash
pytest -q
```

The tests use a small, fully-known synthetic database (see `tests/conftest.py`)
and run without any access to real registry data.

## Local-only git ignores

The shared `.gitignore` covers project-wide generated files. Machine-specific paths
(PreFer checkouts, local R projects, fine-tuning experiments) live in a separate
local file so they are not committed to the repo:

```bash
cp .gitignore.local.example .gitignore.local
git config core.excludesFile .gitignore.local
```

Edit `.gitignore.local` for your own environment; it is never pushed.

## Optional dependencies

The optional token-length / fine-tuning helpers need extra packages:

```bash
pip install -e ".[stats]"    # tiktoken, transformers, datasets
```

## Adding a new data source

See the "Extending BOLT: Adding New Data Sources" section of the `README.md`.
In short:

1. Add a `Paragraph` subclass and an instantiator in
   `serialization/instantiator_scripts/`.
2. Register the instantiator in `serialization/registry.py`.
3. Add (or extend) a synthetic data generator under `synth/` so the new source
   can be exercised without real data.
4. Add a test in `tests/` that asserts the new source renders correctly.

## Guidelines

- Keep changes focused and covered by a test where practical.
- Match the existing code style; avoid introducing new heavy dependencies in the
  core path (keep `transformers`/`datasets`/`tiktoken` behind the `stats` extra).
- Never commit real or individual-level registry data. Only synthetic data
  belongs in this repository.
