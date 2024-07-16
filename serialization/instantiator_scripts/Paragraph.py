"""
The Paragraph class serves as a base class for representing and serializing various types of 
information related to persons in the CBS personal records database.

It includes common attributes that are shared across different paragraph types and provides a framework for 
more specific paragraph classes to build upon.

Attributes:
    year (int): The year the paragraph occurred.
    paragraph_type (str): The category of the paragraph.
    table_name (str): The name of the source database table.
    rinpersoon (int): Unique identifier for the person related to the paragraph.
    paragraph_string (str, init=False): Textual representation of the paragraph (constructed in subclasses).
"""
from dataclasses import dataclass, field, fields
from typing import List, Literal
import json

@dataclass
class Paragraph:
    dataset_name: str
    rinpersoon: int # RINSPERSOON. Is this the main key?
    is_spell: bool = field(default=False)

    year: int = field(default=None)
    month: int = field(default=None)
    day: int = field(default=None)

    feature_transl_dict: dict = field(default_factory=dict)

    

    def __post_init__(self):
        # read the feature translation dictionary from static/feature_translations.json. Use path relative to the project root
        with open('serialization/static/feature_translations.json') as f:
            self.feature_transl_dict = json.load(f)
        

    def get_paragraph_string_tabular(self, excluded_features_list=None):
        # features of parent class are excluded from basic serialization by default
        parent_class_features = [f.name for f in fields(Paragraph)]
        if excluded_features_list:
            excluded_features_list = parent_class_features + excluded_features_list
            attributes = (f"{self.feature_transl_dict[field.name]}: {getattr(self, field.name)}" for field in fields(self) if field.name not in excluded_features_list and getattr(self, field.name))
            return "\n".join(attributes)
        else:
            excluded_features_list = parent_class_features
            attributes = (f"{self.feature_transl_dict[field.name]}: {getattr(self, field.name)}" for field in fields(self) if field.name not in excluded_features_list and getattr(self, field.name))
            return "\n".join(attributes)
        

    def get_paragraph_string_biographic(self):
        pass
