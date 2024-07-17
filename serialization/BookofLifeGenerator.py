
from typing import List
from instantiator_scripts.Paragraph import Paragraph
from instantiator_scripts.PersonAttributesParagraph import PersonAttributesParagraph
from instantiator_scripts.HouseholdEventParagraph import HouseholdEventParagraph
from Recipe import Recipe
from instantiator_scripts.persoon_tab import get_person_attributes
from instantiator_scripts.household_bus import get_households
from operator import attrgetter

class BookofLifeGenerator:
    def __init__(self, rinpersoon, recipe_yaml_path):
        self.rinpersoon = rinpersoon
        self.recipe = Recipe(recipe_yaml_path)
        self.book: str = ""
        self.paragraphs: List[Paragraph] = []
        self.instantiate_paragraphs()


        self.social_context_paragraphs = self.instantiate_social_context_paragraphs(self.recipe.social_context_features)

    def instantiate_paragraphs(self):
        for dataset in self.recipe.datasets:
            dataset_name = dataset.get('name')
            features = self.recipe.get_features(dataset_name)

            if dataset_name == 'persoon_tab':
                ## Add PersonAttributesParagraph to the list of paragraphs
                self.paragraphs.append(get_person_attributes(self.rinpersoon))
            elif dataset_name == 'household_bus':
                ## Add List of HouseholdEventParagraphs to the list of paragraphs
                self.paragraphs.append(get_households(self.rinpersoon))
            else:
                raise ValueError(f"Dataset name {dataset_name} not recognized")
            

    def instantiate_social_context_paragraphs(self, social_context_features):
        result = {}
        for dataset in social_context_features:
            dataset_name = list(dataset.keys())[0]
            result[dataset_name] = {}

            
            for context, features in dataset[dataset_name].items():
                result[dataset_name][context] = BookofLifeGenerator("03c6605f", {
                    'main_key': self.recipe.main_key,
                    'datasets': features,
                    'formatting': {
                        'sorting_keys': self.recipe.sorting_keys,
                        'paragraph_generator': 'get_paragraph_string_tabular'
                    }
                })
        return result



    def sort_paragraphs(self, sorting_keys):
        '''sort paragraphs based on sorting keys.'''

        if isinstance(sorting_keys, str):
            sorting_keys = [sorting_keys]
        
        self.paragraphs.sort(key=attrgetter(*sorting_keys))
        return self.paragraphs

    def write_book(self, generator_function):
        assert self.book == "", "Book is not empty"
        for paragraph in self.paragraphs:
            paragraph_string = getattr(paragraph, generator_function)(self.recipe.get_features(paragraph.dataset_name))
            self.book += "\n\n" + paragraph_string

    def generate_book(self):
        self.sort_paragraphs(self.recipe.sorting_keys)
        self.write_book(self.recipe.paragraph_generator)
        return self.book

    

# Example usage:
generator = BookofLifeGenerator("03c6605f", 'recipes/template.yaml')
# print("Partner:", generator.social_context_paragraphs['household_bus']['partners'].generate_book())
# print("Partner's child:", generator.social_context_paragraphs['household_bus']['partners'].social_context_paragraphs['persoon_tab']['partners'].generate_book())
print('Main book:', generator.generate_book())


# print("Partner's child:", generator.social_context_paragraphs)