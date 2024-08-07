import pandas as pd
import numpy as np
import os

def preprocess_lisa():

    df = pd.read_csv(## TODO: lisa dataset file name ##, 
        index_col=False)

    categorical_cols = ["children_post2021", "GBAGEBOORTELAND", "GBAGESLACHT", "GBAGEBOORTELANDMOEDER",
                        "GBAGEBOORTELANDVADER", "GBAHERKOMSTGROEPERING", "GBAGENERATIE", "GBAGESLACHTMOEDER",
                        "GBAGESLACHTVADER", "GBAHERKOMSTLAND", "GBAGEBOORTELANDNL", "OPLNIVSOI2021AGG4HBmetNIRWO",
                        "OPLNIVSOI2021AGG4HGmetNIRWO", "OPLNIVSOI2021AGG4HBmetNIRWO_isced", "OPLNIVSOI2021AGG4HGmetNIRWO_isced",
                        "SECM", "SCONTRACTSOORT_main", "SPOLISDIENSTVERBAND_main", "GBABURGERLIJKESTAATNW",
                        "RINPERSOONSVERBINTENISP", "RINPERSOONVERBINTENISP", "GBAGEBOORTEMAANDPARTNER",
                        "GBAGESLACHTPARTNER", "PLNIVSOI2021AGG4HBmetNIRWO_partner", "OPLNIVSOI2021AGG4HGmetNIRWO_partner",
                        "OPLNIVSOI2021AGG4HBmetNIRWO_partner_isced", "OPLNIVSOI2021AGG4HGmetNIRWO_partner_isced",
                        "SECM_partner", "INPEMEZ", "INPEMFO", "INPPINK", "INPPOSHHK", "RINPERSOONSHKW", "RINPERSOONHKW",
                        "INHBBIHJ", "INHEHALGR", "INHPOPIIV", "INHSAMAOW", "INHSAMHH", "INHUAFTYP", "SOORTOBJECTNUMMER",
                        "RINOBJECTNUMMER", "VBOWoningtype", "HUISHOUDNR", "TYPHH"]

    # make sure all categorical cols are the correct format
    for col in categorical_cols:
        df[col] = pd.Categorical(df[col])

    # replace numerical 'unknown' values with NaNs
    df.replace(["-", "9999999999", 9999999999], np.nan, inplace=True)
    df["INHAHL"].replace(99, np.nan, inplace=True)
    df["INHAHLMI"].replace(99, np.nan, inplace=True)

    df.to_csv(
            os.path.join('synth', 'data', 'edit', 'lisa_tab.csv'), index=False)

if __name__ == "__main__":
    preprocess_lisa()



