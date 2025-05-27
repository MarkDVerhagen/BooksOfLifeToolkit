from dataclasses import dataclass, field, fields
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
class LisaLocationParagraph(Paragraph):
    """
    The PersonOriginParagraph class is specifically designed for the GBAPERSOONTAB data table.
    It extends the Paragraph class by adding attributes that capture invariant personal information 
    such as country of birth, gender, parents' birth countries, and more.
    name: persoon_tab
    """
    VZAFSTANDKDV: str = field(default=None)
    VZAANTKDV01KM: str = field(default=None)
    VZAANTKDV03KM: str = field(default=None)
    VZAANTKDV05KM: str = field(default=None)
    VZAFSTANDBSO: str = field(default=None)
    VZAANTBSO01KM: str = field(default=None)
    VZAANTBSO03KM: str = field(default=None)
    VZAANTBSO05KM: str = field(default=None)


    def __post_init__(self):
        # super().__post_init__()
        assert self.dataset_name.startswith('loc_lisa_tab'), "This class is specifically designed for the GBAPERSOONTAB data table. Dataset name must be 'persoon_tab'"

        self.year = int(2020)
        self.month = "12"
        self.day = "31"
        self.year_dataset_name = self.dataset_name + '_' + str(self.year)
        self.year_month_day = '_'.join([str(self.year), str(self.month), str(self.day)])
        self.VZAFSTANDKDV = self.VZAFSTANDKDV.replace(".0", "") if self.VZAFSTANDKDV else 'nan' 
        self.VZAANTKDV01KM = self.VZAANTKDV01KM.replace(".0", "") if self.VZAANTKDV01KM else 'nan' 
        self.VZAANTKDV03KM = self.VZAANTKDV03KM.replace(".0", "") if self.VZAANTKDV03KM else 'nan' 
        self.VZAANTKDV05KM = self.VZAANTKDV05KM.replace(".0", "") if self.VZAANTKDV05KM else 'nan' 
        self.VZAFSTANDBSO = self.VZAFSTANDBSO.replace(".0", "") if self.VZAFSTANDBSO else 'nan' 
        self.VZAANTBSO01KM = self.VZAANTBSO01KM.replace(".0", "") if self.VZAANTBSO01KM else 'nan' 
        self.VZAANTBSO03KM = self.VZAANTBSO03KM.replace(".0", "") if self.VZAANTBSO03KM else 'nan' 
        self.VZAANTBSO05KM = self.VZAANTBSO05KM.replace(".0", "") if self.VZAANTBSO05KM else 'nan'