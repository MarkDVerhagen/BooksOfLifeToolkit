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
class LisaIncomeParagraph(Paragraph):
    """
    The PersonOriginParagraph class is specifically designed for the GBAPERSOONTAB data table.
    It extends the Paragraph class by adding attributes that capture invariant personal information 
    such as country of birth, gender, parents' birth countries, and more.
    name: persoon_tab
    """
    INPBELI: str = field(default=None)
    INPEMEZ: str = field(default=None)
    INPEMFO: str = field(default=None)
    INPP100PBRUT: str = field(default=None)
    INPP100PPERS: str = field(default=None)
    INPPERSPRIM: str = field(default=None)
    INPPINK: str = field(default=None)
    INPPOSHHK: str = field(default=None)
    INHAHL: str = field(default=None)
    INHAHLMI: str = field(default=None)
    INHARMEUR: str = field(default=None)
    INHARMEURL: str = field(default=None)
    INHBBIHJ: str = field(default=None)
    INHBRUTINKH: str = field(default=None)

    def __post_init__(self):
        # super().__post_init__()
        assert self.dataset_name.startswith('inc_lisa_tab'), "This class is specifically designed for the GBAPERSOONTAB data table. Dataset name must be 'persoon_tab'"

        self.year = int(2020)
        self.month = "12"
        self.day = "31"
        self.year_dataset_name = self.dataset_name + '_' + str(self.year)
        self.year_month_day = '_'.join([str(self.year), str(self.month), str(self.day)])
        self.INPBELI  = self.INPBELI.replace(".0", "") if self.INPBELI  else 'nan' 
        self.INPEMEZ = self.INPEMEZ.replace(".0", "") if self.INPEMEZ else 'nan' 
        self.INPEMFO = self.INPEMFO.replace(".0", "") if self.INPEMFO else 'nan' 
        self.INPP100PBRUT = self.INPP100PBRUT.replace(".0", "") if self.INPP100PBRUT else 'nan' 
        self.INPP100PPERS = self.INPP100PPERS.replace(".0", "") if self.INPP100PPERS else 'nan' 
        self.INPPERSPRIM = self.INPPERSPRIM.replace(".0", "") if self.INPPERSPRIM else 'nan' 
        self.INPPINK = self.INPPINK.replace(".0", "") if self.INPPINK else 'nan' 
        self.INPPOSHHK = self.INPPOSHHK.replace(".0", "") if self.INPPOSHHK else 'nan' 
        self.INHAHL = self.INHAHL.replace(".0", "") if self.INHAHL else 'nan' 
        self.INHAHLMI = self.INHAHLMI.replace(".0", "") if self.INHAHLMI else 'nan' 
        self.INHARMEUR = self.INHARMEUR.replace(".0", "") if self.INHARMEUR else 'nan' 
        self.INHARMEURL = self.INHARMEURL.replace(".0", "") if self.INHARMEURL else 'nan' 
        self.INHBBIHJ = self.INHBBIHJ.replace(".0", "") if self.INHBBIHJ else 'nan' 
        self.INHBRUTINKH = self.INHBRUTINKH.replace(".0", "") if self.INHBRUTINKH else 'nan' 