from dataclasses import dataclass, field, fields
from typing import List, Literal
from serialization.instantiator_scripts.Paragraph import Paragraph

@dataclass
class EducationEventParagraph(Paragraph):
    """
    The PersonOriginParagraph class is designed for the HOOGSTEOPLTAB data table.
    It extends the Paragraph class by adding attributes that capture information about each person's 
    educational attainment.
    name: education_bus
    """

    ### ORDER OF BELOW IS RELEVANT! ###


    Highest_educational_credential: str = field(default=None)
    Highest_educational_enrolment: str = field(default=None)
    Highest_education_credential_level: str = field(default=None)
    Highest_education_enrolment_level: str = field(default=None)
    Change_year: str = field(default=None)

    def __post_init__(self):
        # super().__post_init__()
        assert self.dataset_name == 'education_bus', "This class is specifically designed for the HOOGSTEOPLTAB data table. Dataset name must be 'education_bus'"

        self.year = int(self.year)
        self.month = "10"
        self.day = "01"

        self.year_dataset_name = self.dataset_name + '_' + str(self.year)
        self.year_month_day = '_'.join([str(self.year), self.month, self.day])
        self.Change_year = str(self.year)
        self.Highest_education_credential_level = self.Highest_education_credential_level.replace(".0", "")
        self.Highest_education_enrolment_level = self.Highest_education_enrolment_level.replace(".0", "")
    def get_paragraph_string_biographic(self, features=None):
        pass