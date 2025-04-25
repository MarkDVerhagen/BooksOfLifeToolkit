## Introduction

This directory contains some data generation scripts for correctness tests.

`actuarial`: Based on age-sex fertility rates in 2023 from StatLine, a set of Books of Life is generated containing age and sex only with outcomes sampled from the true distribution.

Usage:

```bash
python tests/correctness/actuarial.py --sample_size 2000
```