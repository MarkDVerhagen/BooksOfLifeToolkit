from dataclasses import dataclass, field, fields
from typing import Literal
from instantiator_scripts.Paragraph import Paragraph

@dataclass
class CivilStatusEventParagraph(Paragraph):
    """
    The CivilStatusEventParagraph class is designed for the dataset that includes civil status
    information of persons registered in the Municipal Personal Data Administration (GBA).
    It includes attributes such as start and end dates of civil status events, partner information, 
    and more.
    name: civilstatus_bus
    """
    # Date on which a person's civil status is established
    GBAAANVANGBURGERLIJKESTAAT: str = field(default=None)
    
    # Date on which a person's civil status is terminated
    GBAEINDEBURGERLIJKESTAAT: str = field(default=None)
    
    # Current civil state of the person
    GBABURGERLIJKESTAATNW: str = field(default=None)
    
    # Year of birth of a person's partner as recorded in the Basic Registration of Persons (BRP)
    GBAGEBOORTEJAARPARTNER: int = field(default=None)
    
    # Birth month of a person's partner as recorded in the Basic Registration of Persons (BRP)
    GBAGEBOORTEMAANDPARTNER: Literal["--", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] = field(default=None)
    
    # Birth day of a person's partner as recorded in the Basic Registration of Persons (BRP)
    GBAGEBOORTEDAGPARTNER: Literal["--", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"] = field(default=None)
    
    # Country of birth of a person's partner
    GBAGEBOORTELANDPARTNER: str = field(default=None)
    
    # Gender of a person's partner (1: Male, 2: Female, "-": Unknown)
    GBAGESLACHTPARTNER: Literal["1", "2", "-"] = field(default=None)
    
    def __post_init__(self):
        assert self.dataset_name == 'civilstatus_bus', "This class is specifically designed for the GBAPERSOONTAB data table. Dataset name must be 'civilstatus_bus'"

# # Create instances of CivilStatusEventParagraph
# civil_status_data = [
#     CivilStatusEventParagraph(
#         dataset_name="civilstatus_bus",  # Table name
#         person_id=67890,   
#         GBAAANVANGBURGERLIJKESTAAT="19951001",     # Date on which a person's civil status is established
#         GBAEINDEBURGERLIJKESTAAT="19961231",       # Date on which a person's civil status is terminated
#         GBABURGERLIJKESTAATNW="5",                 # Current civil state of the person
#         GBAGEBOORTEJAARPARTNER=1980,               # Year of birth of a person's partner
#         GBAGEBOORTEMAANDPARTNER="05",              # Birth month of a person's partner
#         GBAGEBOORTEDAGPARTNER="01",                # Birth day of a person's partner
#         GBAGEBOORTELANDPARTNER="Netherlands",      # Country of birth of a person's partner
#         GBAGESLACHTPARTNER="1"                     # Gender of a person's partner
#     ),
# ]

# # Convert list of CivilStatusEventParagraph instances to list of dictionaries
# civil_status_data_dict_list = [civil_status.__dict__ for civil_status in civil_status_data]

# # Display the list of dictionaries
# for civil_status in civil_status_data:
#     print(civil_status.get_paragraph_string_tabular())

