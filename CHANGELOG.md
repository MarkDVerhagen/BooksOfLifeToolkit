# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/).

## [0.1.0] - Unreleased

First public release of the Books of Life Toolkit (BOLT).

### Added
- Synthetic data generators (`synth/`) so the full pipeline runs without registry
  access.
- Recipe-driven generation of books of life (`recipes/template.yaml`).
- Social context ("books within books"): household members are discovered,
  classified into partners/children/others, and can be written as nested
  sub-books with a depth guard against infinite regress
  (`recipes/social_context.yaml`).
- Extensible instantiator registry (`serialization/registry.py`).
- Packaging via `pyproject.toml` with `stats` and `dev` extras; split
  `requirements.txt` (core), `requirements-stats.txt`, and `requirements-lock.txt`.
- Test suite (`tests/`) and GitHub Actions CI (lint-free, tests + pipeline smoke).
- `LICENSE` (MIT), `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `CITATION.cff`, and
  issue/PR templates.

### Fixed
- Person attributes were shifted by one column, mislabeling every demographic
  field in every book.
- Synthetic household data used descriptive strings where the instantiator
  expected CBS numeric codes, producing "unknown type"/"unknown place" everywhere.
- `n_spell` filtering kept the wrong spells (now keeps the *n* most recent).
- `REFPERSOONHH` was compared as an integer against a string and always rendered
  "no".

### Changed
- Core book generation no longer requires `transformers`/`datasets`/`tiktoken`
  (now lazy-imported behind the `stats` extra).
- The translation dictionary is loaded once and resolved relative to the package
  (works from any working directory).
- Removed the redundant `populate_db.py` step; `make_db.py` now fully builds the
  database.
