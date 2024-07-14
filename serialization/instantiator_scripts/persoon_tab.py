import pandas as pd
from instantiator_scripts.PersonAttributesParagraph import PersonAttributesParagraph

def get_person_attributes(rinpersoon: int) -> PersonAttributesParagraph:
    # Load the dataset
    df = pd.read_csv('synth/data/persoontab.csv')
    
    # Find the row with the given person_id
    person_row = df[df['rinpersoon'] == rinpersoon]
    person_row = person_row.to_dict(orient="list")
    
    # Create the PersonAttributesParagraph object
    person_attributes = PersonAttributesParagraph(
    dataset_name="persoon_tab",
    rinpersoon=person_row['rinpersoon'][0],
    GBAGEBOORTELAND=person_row['GBAGEBOORTELAND'][0],
    GBAGESLACHT=person_row['GBAGESLACHT'][0],
    GBAGEBOORTEJAAR=person_row['GBAGEBOORTEJAAR'][0],
    GBAHERKOMSTLAND=person_row['GBAHERKOMSTLAND'][0],
    GBAGEBOORTELANDNL=person_row['GBAGEBOORTELANDNL'][0],
    GBAHERKOMSTGROEPERING=person_row['GBAHERKOMSTGROEPERING'][0],
    GBAGENERATIE=person_row['GBAGENERATIE'][0],
    GBAAANTALOUDERSBUITENLAND=person_row['GBAAANTALOUDERSBUITENLAND'][0],
    GBAGEBOORTELANDMOEDER=person_row['GBAGEBOORTELANDMOEDER'][0],
    GBAGESLACHTMOEDER=person_row['GBAGESLACHTMOEDER'][0],
    GBAGEBOORTEJAARMOEDER=person_row['GBAGEBOORTEJAARMOEDER'][0],
    GBAGEBOORTELANDVADER=person_row['GBAGEBOORTELANDVADER'][0],
    GBAGESLACHTVADER=person_row['GBAGESLACHTVADER'][0],
    GBAGEBOORTEJAARVADER=person_row['GBAGEBOORTEJAARVADER'][0],
    )

    
    return person_attributes

# Example usage
# file_path = 'synth/data/persoontab.csv'
# person_id = 12345  # Replace with the actual person_id you want to query
# person_attributes = get_person_attributes(person_id)
# print(person_attributes)