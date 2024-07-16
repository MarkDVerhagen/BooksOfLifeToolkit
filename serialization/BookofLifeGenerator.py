
from typing import List
from instantiator_scripts.Paragraph import Paragraph
from instantiator_scripts.PersonAttributesParagraph import PersonAttributesParagraph
from instantiator_scripts.HouseholdEventParagraph import HouseholdEventParagraph
from Recipe import Recipe
from instantiator_scripts.persoon_tab import get_person_attributes
from operator import attrgetter

class BookofLifeGenerator:
    def __init__(self, rinpersoon, recipe_yaml_path):
        self.rinpersoon = rinpersoon
        self.recipe = Recipe(recipe_yaml_path)
        self.book: str = ""
        self.paragraphs: List[Paragraph] = []

    def instantiate_paragraphs(self):
        for dataset in self.recipe.datasets:
            dataset_name = dataset.get('name')
            excluded_features = self.recipe.get_excluded_features(dataset_name)

            if dataset_name == 'persoon_tab':
                self.paragraphs.append(get_person_attributes(self.rinpersoon))
            elif dataset_name == 'household_bus':
                paragraph = HouseholdEventParagraph(dataset_name, excluded_features)
            else:
                raise ValueError(f"Dataset name {dataset_name} not recognized")
            

    def sort_paragraphs(self, sorting_keys):
        '''sort paragraphs based on sorting keys.'''

        if isinstance(sorting_keys, str):
            sorting_keys = [sorting_keys]
        
        self.paragraphs.sort(key=attrgetter(*sorting_keys))
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
generator = BookofLifeGenerator("03c6605f", 'recipes/template.yaml')
print(generator.generate_book())