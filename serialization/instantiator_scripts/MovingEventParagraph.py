from dataclasses import dataclass, field
from typing import List, Literal
from serialization.instantiator_scripts.Paragraph import Paragraph

def make_date(day, month, year):
    month_names = {
                "01": "Jan",
                "02": "Feb",
                "03": "Mar",
                "04": "Apr",
                "05": "May",
                "06": "Jun",
                "07": "Jul",
                "08": "Aug",
                "09": "Sep",
                "10": "Oct",
                "11": "Nov",
                "12": "Dec"
            }
    month_acronym = month_names.get(month, "unknown month")
    return ' '.join([month_acronym, day, year])


@dataclass
class MovingEventParagraph(Paragraph):
    """The MovingEventParagraph class is designed for the dataset that includes moving data
    name: object_bus
    """
    ## OBJECT_ID
    # Unique object identification number
    Object_id: str = field(default=None)
    # Object type
    VBOWoningtype: str = field(default=None)
    # Natural language description of location
    location_desc: str = field(default=None)
    # Start date of stay
    start_date: str = field(default=None)
    # End date of stay
    end_date: str = field(default=None)

    def __post_init__(self):        
        # super().__post_init__()
        assert self.dataset_name.startswith('object_bus'), "This class is specifically designed for the GBAHUISHOUDENSBUS data table. Dataset name must be 'object_bus'"
        
        # set year, month, and day values of parent class from houshold start date
        year = self.start_date[:4]
        month = self.start_date[5:7]
        day = self.start_date[8:10]

        # Convert them to integers (if needed)
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        
        # Spell start and end
        self.spell_year_end = int(self.end_date[:4])
        self.spell_year_start = int(self.start_date[:4])
        
        # Formatted date
        self.start_date = make_date(self.start_date[8:10],
                                        self.start_date[5:7], self.start_date[:4])
        self.end_date = make_date(self.end_date[8:10],
                                        self.end_date[5:7], self.end_date[:4]) if self.end_date[:4] != "2050" else "Ongoing"

        self.year_dataset_name = self.dataset_name + '_' + str(self.year)
        self.year_month_day = '_'.join([year, month, day])
