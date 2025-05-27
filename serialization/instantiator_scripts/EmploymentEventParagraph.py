from dataclasses import dataclass, field, fields
from typing import Literal
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
class EmploymentEventParagraph(Paragraph):
    """
    The EmploymentEventParagraph class is designed for the dataset that includes employment information
    on jobs and wages of employees at Dutch companies for a given reporting year.
    It includes attributes such as start and end dates of the reporting period, wages, benefits, insurance,
    etc. 
    name: employment_bus
    """
    
    SSOORTBAAN: str = field(default=None)
    SSECT: str = field(default=None)
    SPOLISDIENSTVERBAND: str = field(default=None)
    SCONTRACTSOORT: str = field(default=None)
    SCDAARD: str = field(default=None)
    IKVID: str = field(default=None)
    start_date: str = field(default=None)
    end_date: str = field(default=None)
    mean_salary: str = field(default=None)
    sd_salary: str = field(default=None)
    mean_monthly_hours: str = field(default=None)
    sd_monthly_hours: str = field(default=None)

    def __post_init__(self):
        # super().__post_init__()
        assert self.dataset_name.startswith('employment_bus'), "This class is specifically designed for the SPOLISBUS data table. Dataset name must be 'employment_bus'"

        # set year, month, and day values of parent class from houshold start date
        year = self.start_date[:4]
        month = self.start_date[5:7]
        day = self.start_date[8:10]
        self.year_month_day = '_'.join([year, month, day])

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
                                  self.end_date[5:7], self.end_date[:4]) if self.end_date != "2020-12-31" else "Ongoing"

        self.year_dataset_name = self.dataset_name + '_' + str(self.year)
        self.sd_monthly_hours = self.sd_monthly_hours.replace(".0", "")
        self.sd_salary = self.sd_salary.replace(".0", "")

