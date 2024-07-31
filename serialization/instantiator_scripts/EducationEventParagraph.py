from dataclasses import dataclass, field, fields
from typing import List, Literal
from serialization.instantiator_scripts.Paragraph import Paragraph

@dataclass
class EducationEventParagraph(Paragraph):
    """
    TODO add description
    name: education_tab
    """

    ### ORDER OF BELOW IS RELEVANT! ###

    
    def __post_init__(self):
        super().__post_init__()
        assert self.dataset_name == 'persoon_tab', "This class is specifically designed for the GBAPERSOONTAB data table. Dataset name must be 'persoon_tab'"

        # TODO instantiate parent class attributes suchh as year, month, etc.


    def get_paragraph_string_biographic(self, features=None):
        pass