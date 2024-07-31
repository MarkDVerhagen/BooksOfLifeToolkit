from dataclasses import dataclass, field, fields
from typing import List, Literal
from serialization.instantiator_scripts.Paragraph import Paragraph

@dataclass
class EducationEventParagraph(Paragraph):
    """
    The PersonOriginParagraph class is designed for the HOOGSTEOPLTAB data table.
    It extends the Paragraph class by adding attributes that capture information about each person's 
    educational attainment.
    name: education_tab
    """

    ### ORDER OF BELOW IS RELEVANT! ###

    ## Education number of highest education completed (codes for course of study)
    ## full code is the combined OPLNRHB and OPLNRHG codes:
    ## e.g., 801515 014836 Natural Stone Worker (Natural Stone Worker, Gravework) 
    ## 801516 014836 Natural Stone Worker (Machine Natural Stone Worker)
    OPLNRHB: str = field(default=None)
    OPLNRHG: str = field(default=None)

    #### 2016 SOI classifications 
    ## Highest education level achieved (out of 18 categories)
    OPLNIVSOI2016AGG4HBMETNIRWO: Literal["-"] = field(default=None)
    OPLNIVSOI2016AGG4HGMETNIRWO: Literal["-" ] = field(default=None) # not sure how this var is diff from the above
    ## Highest education level achieved (including estimates for educ not observed in registers)
    RICHTdetailISCEDF2013HBmetNIRWO: Literal["-"] = field(default=None)
    RICHTdetailISCEDF2013HGmetNIRWO: Literal["-" ] = field(default=None) # again not sure how this var is diff from above

    #### 2021 SOI classifications
    OPLNIVSOI2021AGG4HBmetNIRWO: Literal["-" ] = field(default=None)
    OPLNIVSOI2021AGG4HGmetNIRWO: Literal["-" ] = field(default=None)
    ## Highest education level achieved (including estimates for educ not observed in registers)
    RICHTSOI2021SCEDF2013HBNIRWO: Literal["-" ] = field(default=None)
    RICHTSOI2021SCEDF2013HGNIRWO: Literal["-" ] = field(default=None)
    
    def __post_init__(self):
        super().__post_init__()
        assert self.dataset_name == 'education_tab', "This class is specifically designed for the HOOGSTEOPLTAB data table. Dataset name must be 'education_tab'"

        # TODO instantiate parent class attributes such as year, month, etc.
        # year is extracted from filename: (1999-2022) HOOGSTEOPLJJJJTABVV: year = JJJJ
        self.month = "10"
        self.day = "01"



    def get_paragraph_string_biographic(self, features=None):
        pass