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
class LisaPartnerParagraph(Paragraph):
    """
    The PersonOriginParagraph class is specifically designed for the GBAPERSOONTAB data table.
    It extends the Paragraph class by adding attributes that capture invariant personal information 
    such as country of birth, gender, parents' birth countries, and more.
    name: persoon_tab
    """
    marriages_total : str = field(default=None)
    partnerships_total: str = field(default=None)
    GBABURGERLIJKESTAATNW: str = field(default=None)
    AANVANGVERBINTENIS: str = field(default=None)
    GBAGEBOORTEJAARPARTNER: str = field(default=None)
    GBAGEBOORTEMAANDPARTNER: str = field(default=None)
    GBAGEBOORTELANDPARTNER: str = field(default=None)
    GBAGESLACHTPARTNER: str = field(default=None)
    OPLNIVSOI2021AGG4HBmetNIRWO_partner: str = field(default=None)
    OPLNIVSOI2021AGG4HGmetNIRWO_partner: str = field(default=None)
    SECM_partner: str = field(default=None)
    children_pre2021: str = field(default=None)

    def __post_init__(self):
        # super().__post_init__()
        assert self.dataset_name.startswith('par_lisa_tab'), "This class is specifically designed for the GBAPERSOONTAB data table. Dataset name must be 'persoon_tab'"

        self.year = int(2020)
        self.month = "12"
        self.day = "31"
        self.year_dataset_name = self.dataset_name + '_' + str(self.year)
        self.year_month_day = '_'.join([str(self.year), str(self.month), str(self.day)])
        self.marriages_total = self.marriages_total.replace(".0", "")
        self.partnerships_total = self.partnerships_total.replace(".0", "")
        self.GBABURGERLIJKESTAATNW = self.GBABURGERLIJKESTAATNW.replace(".0", "") if self.GBABURGERLIJKESTAATNW else 'nan' 
        self.AANVANGVERBINTENIS = make_date(self.AANVANGVERBINTENIS[6:8], self.AANVANGVERBINTENIS[4:6], self.AANVANGVERBINTENIS[:4])
        self.GBAGEBOORTEJAARPARTNER = self.GBAGEBOORTEJAARPARTNER.replace(".0", "") if self.GBAGEBOORTEJAARPARTNER else 'nan' 
        self.GBAGEBOORTEMAANDPARTNER = self.GBAGEBOORTEMAANDPARTNER.replace(".0", "") if self.GBAGEBOORTEMAANDPARTNER else 'nan' 
        self.GBAGEBOORTELANDPARTNER = self.GBAGEBOORTELANDPARTNER.replace(".0", "") if self.GBAGEBOORTELANDPARTNER else 'nan' 
        self.GBAGESLACHTPARTNER = self.GBAGESLACHTPARTNER.replace(".0", "") if self.GBAGEBOORTELANDPARTNER else 'nan' 
        self.OPLNIVSOI2021AGG4HBmetNIRWO_partner = self.OPLNIVSOI2021AGG4HBmetNIRWO_partner.replace(".0", "") if self.OPLNIVSOI2021AGG4HBmetNIRWO_partner else 'nan' 
        self.OPLNIVSOI2021AGG4HGmetNIRWO_partner = self.OPLNIVSOI2021AGG4HGmetNIRWO_partner.replace(".0", "") if self.OPLNIVSOI2021AGG4HGmetNIRWO_partner else 'nan' 
        self.SECM_partner = self.SECM_partner.replace(".0", "") if self.SECM_partner else 'nan' 