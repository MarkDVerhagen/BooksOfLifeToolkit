# prefer_prepare

This repository contains code to prepare the analytical pipeline for PreFer Stage 2.

## Getting Started

1. **Clone the repository**

2. **Set up virtual environment (recommended).**
```
python3 -m venv myenv  
source myenv/bin/activate
```

3. **Install requirements.**
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

### Overview

The `serialization` module generates personalized "books of life" text containing life events and information related to a person in the dataset(s). The `BookofLifeGenerator` class is the core component, which reads data from various datasets, organizes it (using the `Paragraph` class), and produces a structured book.

### Supported Features

- **Data Parsing**: Reads life event and personal attributes data from multiple datasets into `Paragraph` objects.
- **Sorting and Organizing**: Sorts `Paragraph` objects by configurable keys.
- **Customization**: Allows for custom formatting and feature extraction.
- **Social Context Integration**: Integrates social context paragraphs.

### Usage

#### Generating Books of Life

1. **Prepare your data**: Ensure your datasets are ready and conform to the expected formats.

2. **Define your recipe**: Create a YAML file that specifies the datasets and features to be used.

3. **Generate the book**:
The following code snippet prints the Book of Life for person `"03c6605f"`.

    ```python
    from serialization import BookofLifeGenerator 

    rinpersoon = "03c6605f"
    recipe_yaml_path = "path/to/your/recipe.yaml"

    generator = BookofLifeGenerator(rinpersoon, recipe_yaml_path)
    book = generator.generate_book()

    # Output the book
    print(book)
    ```
