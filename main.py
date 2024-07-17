from serialization import BookofLifeGenerator

# Example usage:
generator = BookofLifeGenerator("03c6605f", 'recipes/template.yaml')
# print("Partner:", generator.social_context_paragraphs['household_bus']['partners'].generate_book())
# print("Partner's child:", generator.social_context_paragraphs['household_bus']['partners'].social_context_paragraphs['persoon_tab']['partners'].generate_book())
print('Main book:', generator.generate_book())
# print("Partner's child:", generator.social_context_paragraphs)


### TODO write main for loop to geenrate and store BoLs here