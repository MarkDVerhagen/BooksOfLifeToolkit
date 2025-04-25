# Books of Life Toolbox (BOLT)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](www.google.com) TODO REPlACE STICKER WITH ACTUAL DOI

This repository contains the **Books of Life Toolbox (BOLT)**, a framework designed to parse rich, structured social science data (like registry data, surveys, logs) into textual life sequences, or "Books of Life" (BoLs). This approach allows researchers to leverage the power of Large Language Models (LLMs) for analyzing complex life trajectories, moving beyond the traditional "X matrix" paradigm.

## Introduction: Embracing the "Bitter Lesson"

As detailed in our accompanying paper "Life Course Analysis in the Time of LLMs", there's a growing tension between the richness of modern social data and the methods traditionally used to analyze it. Formatting complex, longitudinal, hierarchical, and networked data into a flat "X matrix" for GLMs or standard machine learning often leads to information loss and requires extensive, task-specific feature engineering.

Inspired by the "bitter lesson" in computer science (Sutton, 2019), which suggests that scalable, general-purpose methods eventually outperform human-designed feature engineering, BOLT provides a way to represent complex social data as text. This approach aims to:

1.  **Preserve Information:** Minimize data loss during preprocessing.
2.  **Leverage LLMs:** Create data representations amenable to powerful LLM techniques.
3.  **Increase Harmony:** Better align the complexity of social data with the methods used for analysis.
4.  **Facilitate Experimentation:** Allow researchers to easily define and generate different textual representations based on theoretical needs or modeling constraints.

This toolkit was initially developed for the [PreFer](https://preferdatachallenge.nl/) computational social science challenge, focused on predicting fertility using Dutch population registry data.

## Key Concepts & Design

BOLT is built around several core concepts:

1.  **Books of Life (BoLs):** The primary output. A textual representation with attributes of a specific unit of analysis (e.g., a person, a household) based on available data sources.
2.  **Paragraphs:** The building blocks of a BoL. Each paragraph typically corresponds to a single record or event from an information source (e.g., a row in a table, a specific spell).
3.  **Instantiation:** The process of converting raw data from various sources into structured `Paragraph` objects. This involves identifying key variables:
    *   **Identifiers:** Link records for the main unit of analysis (e.g., `rinpersoon`).
    *   **Hierarchy Variables:** Link related entities (e.g., `hh_id` to link household members, employer ID to link coworkers).
    *   **Temporal Variables:** Define the time and sequence of events (e.g., `start_date`, `end_date`).
    *   **Content Variables:** All other information to be included in the paragraph text.
4.  **Recipes (`*.yaml`):** Configuration files that define *how* to build a BoL. They specify:
    *   The **unit of analysis** identifier.
    *   The **information sources** to include.
    *   **Filtering rules** for paragraphs (e.g., based on date, content, or sequence position).
    *   **Hierarchy rules** for including information about related entities (e.g., fetching data for household members).
    *   **Parsing and ordering** instructions for generating the final text.
5.  **Modularity (`serialization/instantiator_scripts/`):** New data sources can be integrated by creating dedicated Python classes (inheriting from `Paragraph` or a specialized base) that handle the instantiation logic for that source.


## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/markdverhagen/prefer_prepare.git # Or your repo URL
    cd prefer_prepare
    ```

2.  **Set up a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```

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
    This script initializes an empty DuckDB database file named `synthetic_data.duckdb`.
    ```bash
    python serialization/make_db.py
    ```
    *(Note: This currently just creates the file; the schema is implicitly defined during population.)*

3.  **Populate Database:**
    This script reads the synthetic data files generated in step 1 and loads them into the `synthetic_data.duckdb` database. It uses the `recipes/template.yaml` file to understand which synthetic data sources correspond to which tables/schemas.
    ```bash
    python serialization/populate_db.py --yaml_file template
    ```

4.  **Generate All Books of Life:**
    This script generates BoLs for the synthetic population, splitting them into train/test sets based on household information from a specific year (as defined in `main.py`), includes a dummy outcome variable, and saves them as sharded JSONL files.
    ```bash
    # Creates ./my_bol_run/data/{train|test}/shard_*.jsonl files
    python main.py --bol_name my_bol_run --recipe_name template --max_processes 4 --save_summary
    ```
    *   `--bol_name`: Specifies the output directory name.
    *   `--recipe_name`: Uses `recipes/template.yaml` to define how BoLs are constructed.
    *   `--max_processes`: Number of parallel processes to use. Adjust based on your machine.
    *   `--save_summary`: Generates token length statistics after completion.

    Check the `my_bol_run/data/` directory for the output files. Each line in the `.jsonl` files contains a JSON object with `rinpersoon`, `book_content`, and `outcome`.

5.  **Generate a Single Book of Life (for Testing/Debugging):**
    This script is useful for inspecting the BoL for a specific individual. It uses the default hash `00721713` (ensure this hash exists in your generated synthetic data).
    ```bash
    python main_test.py --hash "00721713" --recipe template
    ```
    *(If `00721713` doesn't exist, find a valid `rinpersoon` hash from `synthetic_data.duckdb` after population or from the output of `main.py` and use that value for `--hash`)*.

## Usage Details

*   **Large-Scale Generation (`main.py`):**
    *   Use `main.py` for generating BoLs for entire datasets.
    *   It handles parallel processing (`--max_processes`) for efficiency.
    *   It includes logic for train/test splitting based on household data (currently hardcoded for the synthetic data structure).
    *   It incorporates an outcome variable (modify the logic within `main.py` for different outcome definitions).
    *   Outputs are sharded JSONL files suitable for LLM fine-tuning pipelines.
    *   Key arguments:
        *   `--bol_name`: Name for the output data directory (required).
        *   `--recipe_name`: Name of the recipe file (without `.yaml`) in the `recipes` directory (required).
        *   `--max_processes`: Number of CPU cores for parallel generation (default: 4).
        *   `--shard_size`: Number of BoLs per output JSONL file (default: 10000).
        *   `--output_dir`: Optional parent directory to save the `bol_name` directory into.
        *   `--save_summary`: Flag to generate and save token count statistics.

*   **Single BoL Generation (`main_test.py`):**
    *   Use `main_test.py` primarily for debugging recipes or inspecting the output for a specific individual.
    *   Requires `--hash` (the identifier of the unit of analysis) and `--recipe` (the recipe name).
    *   Prints the generated BoL to the console.

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
