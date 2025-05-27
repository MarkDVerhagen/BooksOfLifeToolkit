from dataclasses import dataclass, field, fields
from typing import List, Literal
from serialization.instantiator_scripts.Paragraph import Paragraph

@dataclass
class StorkParagraph(Paragraph):
    """
    The PersonOriginParagraph class is specifically designed for the GBAPERSOONTAB data table.
    It extends the Paragraph class by adding attributes that capture invariant personal information 
    such as country of birth, gender, parents' birth countries, and more.
    name: persoon_tab
    """
    p: str = field(default=None)
    
    def __post_init__(self):
        # super().__post_init__()
        assert self.dataset_name.startswith('stork'), "This class is specifically designed for the stork oracle data table. Dataset name must be 'stork_tab'"

        self.year = int(2020)
        self.month = "12"
        self.day = "31"
        self.year_dataset_name = self.dataset_name + '_' + str(self.year)
        self.year_month_day = '_'.join([str(self.year), str(self.month), str(self.day)])
        self.p = f"{self.p}%".replace(".0", "")
        self.stork1 = f"Another model predicts that there is a {self.p}% chance that this person has a child between 2021 and 2023"
        self.stork2 = f"Another prediction: {self.p}%"