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
import os
from dataclasses import dataclass, field, fields
from typing import List, Literal
import json
from abc import ABC, abstractmethod

# Path to the field/value translation dictionary, resolved relative to this file
# so it works regardless of the current working directory.
_FEATURE_TRANSLATIONS_PATH = os.path.join(
    os.path.dirname(__file__), os.pardir, "static", "feature_translations.json"
)

_FEATURE_TRANSLATIONS = None


def get_feature_translations():
    """Load (and cache) the field/value translation dictionary once."""
    global _FEATURE_TRANSLATIONS
    if _FEATURE_TRANSLATIONS is None:
        with open(_FEATURE_TRANSLATIONS_PATH) as f:
            _FEATURE_TRANSLATIONS = json.load(f)
    return _FEATURE_TRANSLATIONS


@dataclass
class Paragraph:
    dataset_name: str
    rinpersoon: str
    is_spell: bool = field(default=False)
    explicit: bool = field(default=True)
    order: int = field(default=0)

    year: int = field(default=None)
    month: int = field(default=None)
    day: int = field(default=None)
    year_dataset_name: str = field(default=None)
    year_month_day: str = field(default=None)

    # def __post_init__(self):
        # read the feature translation dictionary from static/feature_translations.json. Use path relative to the project root

    def get_paragraph_string_tabular(self, features=None):
        # features of parent class are excluded from basic serialization by default
        parent_class_features = [f.name for f in fields(Paragraph)]
        feature_transl_dict = get_feature_translations()
        
        def is_valid(value):
            return value is not None and value != 'nan' and (not isinstance(value, list) or value) and value != "----" and value != ''

        if self.explicit:
            if features:
                attributes = (f"{feature_transl_dict[field.name]}: {getattr(self, field.name)}" for field in fields(self) if field.name in features and getattr(self, field.name))
                return "\n".join(attributes)
            else:
                excluded_features_list = parent_class_features
                attributes = (f"{feature_transl_dict[field.name]}: {getattr(self, field.name)}" for field in fields(self) if field.name not in excluded_features_list and getattr(self, field.name))
                return "\n".join(attributes)
        else:
            if features:
                attributes = (f"{feature_transl_dict[field.name]}: {getattr(self, field.name)}" for field in fields(self) if field.name in features and is_valid(getattr(self, field.name)))
                return "\n".join(attributes)
            else:
                excluded_features_list = parent_class_features
                attributes = (f"{feature_transl_dict[field.name]}: {getattr(self, field.name)}" for field in fields(self) if field.name not in excluded_features_list and is_valid(getattr(self, field.name)))
                return "\n".join(attributes)
        
    @abstractmethod
    def get_paragraph_string_biographic(self):
        pass
