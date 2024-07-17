import pandas as pd
from instantiator_scripts.HouseholdEventParagraph import HouseholdEventParagraph

'''This function loads all households for a given rinpersoon (person_id)
by creating a list of HouseholdEventParagraph objects'''

def get_households(rinpersoon: int) -> list[HouseholdEventParagraph]:

    # Load the dataset
    df = pd.read_csv('synth/data/edit/householdbus.csv')
    
    # Filter rows related to the given rinpersoon
    households_df = df[df['rinpersoon'] == rinpersoon]
    
    # Create a list to hold HouseholdEventParagraph objects
    household_paragraphs = []
    
    # Iterate over each row to create HouseholdEventParagraph objects
    for _, row in households_df.iterrows():
        household_paragraph = HouseholdEventParagraph(
            dataset_name="household_bus",
            HOUSEKEEPING_NR=row['HOUSEKEEPING_NR'],
            TYPHH=row['TYPHH'],
            DATE_STIRTHH=row['DATE_STIRTHH'],
            DATUMEINDEHH=row['DATUMEINDEHH'],
            NUMBERPERSHH=row['NUMBERPERSHH'],
            PLHH=row['PLHH'],
            REFPERSOONHH=row['REFPERSOONHH'],
            AANTALOVHH=row['AANTALOVHH'],
            AANTALKINDHH=row['AANTALKINDHH'],
            BIRTHEDYOUNGCHILDHH=row['BIRTHEDYOUNGCHILDHH'],
            GEBMAANDJONGSTEKINDHH=row['GEBMAANDJONGSTEKINDHH'],
            GEBJAAROUDSTEKINDHH=row['GEBJAAROUDSTEKINDHH'],
            BMAANDOUDSTEKINDHH=row['BMAANDOUDSTEKINDHH'],
            CHILDREN=[], #not implemented
            PARTNERS=[],  # Assuming there are no explicit partner lists in the data provided
            OTHER_MEMBERS=[],  # Assuming there are no explicit other members lists in the data provided
            ALL_MEMBERS=row['ID_list_rinpersoon']
        )
        household_paragraphs.append(household_paragraph)
    
    return household_paragraphs


##Example usage
person_id = '71ed4a86' # Replace with the actual person_id you want to query
households = get_households(person_id)
for household in households:
    print(households)