
from typing import List
from Paragraph import Paragraph
from PersonAttributesParagraph import PersonAttributesParagraph
from HouseholdEventParagraph import HouseholdEventParagraph
from Recipe import Recipe

class BookofLifeGenerator:
    def __init__(self, recipe_yaml_path):
        self.recipe = Recipe(recipe_yaml_path)
        self.book: str = ""
        self.paragraphs: List[Paragraph] = []

    def instantiate_paragraphs(self):
        for dataset in self.recipe.datasets:
            dataset_name = dataset.get('name')
            excluded_features = self.recipe.get_excluded_features(dataset_name)

            if dataset_name == 'persoon_tab':
                paragraph = PersonAttributesParagraph(dataset_name, excluded_features)
            elif dataset_name == 'household_bus':
                paragraph = HouseholdEventParagraph(dataset_name, excluded_features)
            else:
                raise ValueError(f"Dataset name {dataset_name} not recognized")
            
            self.paragraphs.append(paragraph)

    def sort_paragraphs(self, sorting_keys):
        # TODO: sort paragraphs based on sorting keys. order of keys specified hierachy of what to sort on first
        return self.paragraphs

    
    def write_book(self, generator_function):
        assert self.book == "", "Book is not empty"
        for paragraph in self.paragraphs:
            paragraph_string = getattr(paragraph, generator_function)()
            self.book += "\n\n" + paragraph_string

    def generate_book(self):
        self.instantiate_paragraphs()
        self.sort_paragraphs(self.recipe.sorting_keys)
        self.write_book(self.recipe.paragraph_generator)
        return self.book

    

# Example usage:
generator = BookofLifeGenerator('recipes/template.yaml')
print(generator.generate_book())