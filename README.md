# prefer_prepare

This repository contains code to prepare the analytical pipeline for PreFer Stage 2.

## Install requirements

1. Set up virtual environment (recommended)
```
python3 -m venv myenv  
source myenv/bin/activate
```

2. Install requirements
```
pip install -r requirements.txt
```

## Synthetic Data

`synth`: folder containing scripts to generate synthetic data

To generate synthetic data for the householdbus (household structure over time), persoontab (characteristics at birth) and vektistab (medical activities) run:


```bash
python3 synth/main.py
```

## Serializing Books of Life

To be continued.