
from typing import List
from serialization.instantiator_scripts.Paragraph import Paragraph
from serialization.instantiator_scripts.PersonAttributesParagraph import PersonAttributesParagraph
from serialization.instantiator_scripts.HouseholdEventParagraph import HouseholdEventParagraph
from serialization.Recipe import Recipe
from serialization.instantiator_scripts.persoon_tab import get_person_attributes
from serialization.instantiator_scripts.household_bus import get_households
from serialization.instantiator_scripts.education_bus import get_education_events
from serialization.instantiator_scripts.employment_bus import get_employment_events
from serialization.instantiator_scripts.object_bus import get_objects
from operator import attrgetter
import duckdb
import json

class BookofLifeGenerator:
    def __init__(self, rinpersoon, recipe_yaml_path, paragraphs, table_version=""):
        self.rinpersoon = rinpersoon
        self.recipe = Recipe(recipe_yaml_path)
        self.book: str = ""
        self.paragraphs = paragraphs
        # self.db_path = db_path
        self.table_version = table_version
        # self.conn = duck_db_conn
        # self.instantiate_paragraphs()

    def sort_paragraphs(self):
        '''sort paragraphs based on sorting keys.'''
        
        ## Start by adding custom keys if present
        # getattr(paragraph, )
        
        sorting_keys = self.recipe.sorting_keys

        if isinstance(sorting_keys, str):
            sorting_keys = [sorting_keys]
        
        supported_sorting_keys = ['year', 'dataset_name', 'year_dataset_name',
                                  'year_month_day']

        # Assert that all elements in sorting_keys are either 'year' or 'dataset_name'
        assert all(key in supported_sorting_keys for key in sorting_keys), "sorting_keys contains values outside of 'year' and 'dataset_name'"

        sorting_keys = ['order'] + sorting_keys

        self.paragraphs.sort(key=attrgetter(*sorting_keys))

        new_pars = []
        for info in self.recipe.datasets:
            sub_pars = []
            name = info.get('name')
            n_spell = info.get('n_spell', None)
            sort_key = info.get('sort_key', None)
            min_spell_year = info.get('min_spell_year', None)
            max_spell_year = info.get('max_spell_year', None)
            sub_pars = [p for p in self.paragraphs if p.dataset_name == str(name)]
            
            if n_spell:
                try:
                    addition = sub_pars[n_spell:]
                except IndexError:
                    addition = []
            else:
                addition = sub_pars
            if not isinstance(addition, list):
                addition = [addition]
            
            if min_spell_year:
                if addition:
                    addition = [a for a in addition if a.spell_year_start >= min_spell_year or a.spell_year_end >= min_spell_year]
            if max_spell_year:
                if addition:
                    addition = [a for a in addition if a.spell_year_start <= max_spell_year or a.spell_year_end <= max_spell_year]
            new_pars.extend(addition)
            
        self.paragraphs = new_pars

        self.paragraphs.sort(key=attrgetter(*sorting_keys))

        return self.paragraphs

    def write_book(self, generator_function):
        assert self.book == "", "Book is not empty"
        for paragraph in self.paragraphs:
            paragraph_string = getattr(paragraph, generator_function)(self.recipe.get_features(paragraph.dataset_name))
            self.book += "\n\n" + paragraph_string

    def generate_book(self):
        self.sort_paragraphs()
        self.write_book(self.recipe.paragraph_generator)

        if self.recipe.formatting.get('header', False):
            self.book += f"\n\nThis was the Book of Life of {self.rinpersoon}."

        return self.book

    