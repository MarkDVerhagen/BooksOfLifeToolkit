# Books of Life Toolbox (BOLT)

[![DOI](https://img.shields.io/badge/arXiv-2507.03027-b31b1b.svg)](https://doi.org/10.48550/arXiv.2507.03027)

This repository contains the **Books of Life Toolbox (BOLT)**, a framework designed to turn complex social data into plain‑text “Books of Life” (BoLs) that can be read by Large Language Models.

## Why BOLT?
Social scientists have long navigated a trade‑off between depth—rich single‑case narratives analysed qualitatively—and scale—large‑N datasets analysed quantitatively. Two recent developments make it possible to explore whether we can have both:

1. Complex log data that cover many facets of social life but are not recorded as a conventional survey.

2. LLMs with exceptional pattern‑recognition abilities on free text.

BOLT bridges the two by programmatically writing out life events, contexts, and relationships into human‑readable narrative summaries—Books of Life—at scale.

## What does BOLT offer?

We designed BOLT along the following principles.

1. **Loss‑minimal representation:** keeps longitudinal, hierarchical, and network structure that is usually flattened away.

2. **LLM‑ready format:** immediate compatibility with GPT‑style prompting, retrieval‑augmented generation, and fine‑tuning.

3. **Composable templates:** declaratively specify which variables, time windows, or social relations to narrate.

4. **Scalable pipeline:** processes registry‑scale data on standard cluster hardware.

5. **Researcher‑friendly recipe:** swap in alternative theories of the life course by editing a single recipe file.

This toolkit was initially developed for the [PreFer](https://preferdatachallenge.nl/) computational social science challenge, focused on predicting fertility using Dutch population registry data.

## Key Concepts & Design

BOLT is built around several core concepts:

1.  **Books of Life (BoLs):** The primary output. A textual representation with attributes of a specific unit of analysis (e.g., a person, a household) based on available data sources.
2.  **Paragraphs:** The building blocks of a BoL. Each paragraph typically corresponds to a single record from some information source (e.g., a row in a table).
3.  **Instantiation:** The process of converting raw data from various sources into structured `Paragraph` objects. This is done by  instantiator functions that are custom made per information source and define relevant fields like time and identifiers.
4.  **Recipes (`*.yaml`):** Configuration files that define *how* to build a BoL. They specify:
    *   The **unit of analysis** identifier.
    *   The **information sources** to include.
    *   **Nested Social Context** for including information about related entities (e.g., fetching data for household members).
    *   **Formatting and ordering** instructions for writing the final BoL.

<p align="center">
  <img src="https://github.com/MarkDVerhagen/prefer_prepare/blob/4adac4a7899abe585ad60b90e33cdf598e36e1a5/bolt_workflow.png" alt="BOLT overview" width="800"/>
</p>

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MarkDVerhagen/BooksOfLifeToolkit.git
    cd BooksOfLifeToolkit
    ```

2.  **Set up a Python 3.12 virtual environment (recommended):**
  Make sure you have Python 3.12 installed. You can check your version with:
  ```bash
  python3.12 --version
  ```
  Create and activate a virtual environment:
  ```bash
  python3.12 -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  ```
  If you don't have Python 3.12, download it from [python.org](https://www.python.org/downloads/release/python-3120/) or use a package manager (e.g., `brew install python@3.12` on macOS).

3.  **Install requirements:**
    ```bash
    pip install -r requirements.txt
    ```

## Quickstart: Generating Books of Life from Synthetic Data

This quickstart uses synthetic data to demonstrate the end-to-end workflow.

1.  **Generate Synthetic Data:**
    This script creates synthetic datasets mimicking registry data (household spells, employment, etc.) and saves them (likely in `synth/data/edit/` or similar, based on `populate_db.py`'s expectations).
    ```bash
    python synth/main.py
    ```

2.  **Create Database Schema:**
    This script reads in a configuration file that defines which datasets are relevant for the desired books of life. It reads these datasets, performs basic wrangling and writes to an edit folder. In parallel, an empty DuckDB database file is generated in line with these datasets.
    
    ```bash
    python serialization/make_db.py --data_dir synth/data --yaml_file recipes/make_db --db_name db
    ```

3.  **Populate Database:**
    This script reads the data files from the edit folder and loads them into the database.
    ```bash
    python serialization/populate_db.py --yaml_file recipes/template --db_name db.duckdb --data_dir synth/data
    ```

4.  **Generate All Books of Life:**
    This script generates BoLs for the synthetic population, splitting them into train/test sets based on household information from a specific year (as defined in `main.py`), includes a dummy outcome variable, and saves them as sharded JSONL files.
    ```bash
    python main.py --db_path db.duckdb --recipe_path recipes/template --output_dir output
    ```

5.  **Generate a Single Book of Life (for Testing/Debugging):**
    This script is useful for inspecting the BoL for a specific individual. It uses the default hash `00721713` (ensure this hash exists in your generated synthetic data).
    ```bash
    python main_test.py --hash "0006861b" --recipe template --db_path db.duckdb
    ```
    *(If `0006861b` doesn't exist, find a valid `rinpersoon` hash from `db.duckdb` after population or from the output of `main.py` and use that value for `--hash`)*.
    

## Understanding Recipes (`recipes/*.yaml`)

Recipes are the core configuration for BOLT, defining the structure and content of the Books of Life. They follow the 3-step conceptual process:

1.  **`main_key:`** (Step 1: Choose Unit of Analysis) Specifies the primary key for the unit of analysis (e.g., `rinpersoon`; so far we only support this).
2.  **`datasets:`** (Step 2 & 3: Determine & Filter Information) A list of data sources to include. Each source specifies:
    *   `name:` Matches the table name in the database (or a logical name).
    *   `features:` Defines which features to include in the book. Available features can be seen from the `Paragraph`class of the respective dataset.
    *   `social_context_features:` Defines whether to recursively instantiate Paragraph objects for related entities (e.g., using `CHILDREN` and `PARTNERS` to recursively generate BoLs for household members using a nested recipe). See `recipes/template.yaml` and below for an example.
3.  **`formatting:`** (Step 4: Generate the Book) Controls the final output generation:
    *   `sorting_keys:` How paragraphs are ordered (you can select any attribute part of the `Paragraph` class).
    *   `paragraph_generator:` How paragraphs are formatted (`machine` for `key: value` pairs, `natural` for more sentence-like structures based on templates).
  
Example:
```main_key: rinpersoon
datasets:
  - name: persoon_tab
    features:
      - GBAGEBOORTEMAAND
      - GBAGEBOORTEDAG
      - GBAGEBOORTEJAARVADER
      - GBAGESLACHTVADER
  - name: household_bus
    features:
    social_context_features:
      PARTNERS:
          - name: household_bus
            features:
              - GBAGESLACHT
            social_context_features:
              CHILDREN:
                  - name: persoon_tab
                    features:
                      - GBAGEBOORTEJAARMOEDER
      CHILDREN: 
        - name: persoon_tab
          features:
            - GBAGESLACHT
  - name: education_bus
    features:
      - OPLNRHB
      - OPLNIVSOI2016AGG4HGMETNIRWO
      - OPLNIVSOI2021AGG4HBmetNIRWO
  - name: employment_bus
    features:
      - SIMPUTATIE
      - SEXTRSAL
      - SPRWAOAOK
      - SINLEGLEVENSLOOP
      - SCDAGH
      - SOPGRCHTEXTRSAL
formatting:
  sorting_keys: # list of keys to sort the paragraphs on. Order indicates priority.
      - year
  paragraph_generator: get_paragraph_string_tabular
```

Explore the files in the `recipes/` directory for more examples.

## Extending BOLT: Adding New Data Sources

To add support for a new data source (e.g., a new registry table):

1.  **Create an Instantiator Class:** Add a new Python file in `serialization/instantiator_scripts/`. Create a class that inherits from `Paragraph` (or a relevant base like `HouseholdEventParagraph.py`).
2.  **Add Instantiator Function:** Add a new Python file in `serialization/instantiator_scripts/` that instantiates the Paragraph object for the respective dataset and person. E.g. `househould_bus.py`
3.  **Update `populate_db.py`:** Modify this script to handle loading your new synthetic or real data source into the DuckDB database, ensuring the table name matches what your instantiator expects. You might also need to adjust `make_db.py` if explicit schema definition is required.
4.  **Update BookOfLifeGenerator Class:** Add your new instantiator script in the constructor of the BookOfLifeGenerator Class to include it. 

## Connection to LLM Fine-tuning

The JSONL files generated by `main.py` are designed as input for supervised fine-tuning (SFT) of Large Language Models. The `book_content` serves as the input/prompt, and the `outcome` serves as the target label/completion.

*   The `hf_pipeline_MWE/` directory contains examples using Hugging Face Transformers (`trl`, `accelerate`).
*   The `torchtune_fine_tuning_MWE/` directory contains examples using PyTorch `torchtune`.

These directories show how BoLs generated by this toolkit can be used in downstream modeling tasks.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs, feature requests, or improvements.

## Citation

If you use BOLT or the concepts presented in our work, please cite our paper:

```bibtex
@article{VerhagenBOLT2025,
  title={Life Course Analysis in the Time of LLMs},
  author={Verhagen, Mark and Stroebl, Benedikt and Liu, Tiffany and Liu, Lydia T. and Salganik, Matthew},
  journal={Journal of Computational Social Science},
  year={2025},
  note={DRAFT April 25, 2025},
  url = {https://github.com/markdverhagen/prefer_prepare}
}
