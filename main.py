from BookofLifeGenerator import BookofLifeGenerator
import pandas as pd
import random

synth_hh = pd.read_csv(os.path.join('synth', 'data', 'edit', 'household_bus.csv'))

synth_hh = synth_hh.\
    loc[synth_hh['DATE_STIRTHH'] == '1998-01-01']

final_year_rins = synth_hh['rinpersoon'].loc[synth_hh['PLHH'] != 'child living at home'].unique()
final_year_hhs = synth_hh['HOUSEKEEPING_NR'].unique()

train_hhs = random.sample(list(final_year_hhs), round(0.8*len(final_year_hhs)))
test_hhs = [i for i in final_year_hhs if i not in train_hhs]

train_rins = list(synth_hh['rinpersoon'].loc[synth_hh['HOUSEKEEPING_NR'].isin(train_hhs)])
test_rins = list(synth_hh['rinpersoon'].loc[~synth_hh['HOUSEKEEPING_NR'].isin(train_hhs)])

train_rins = [i for i in train_rins if i in final_year_rins]
test_rins = [i for i in test_rins if i in final_year_rins]

for recipe in ['test_template1', 'test_template2']:
    bol_train = [BookofLifeGenerator(rin, './recipes/' + recipe + '.yaml').generate_book() for rin in train_rins]
    bol_test = [BookofLifeGenerator(rin, './recipes/' + recipe + '.yaml').generate_book() for rin in test_rins]

    for text, title in zip(bol_train, train_rins):
        filename = f"{title}.txt"
        with open(os.path.join('synth', 'data', 'e2e', 'test_template1', 'train',
                            'bol', filename), 'w') as file:
            file.write(text)
        print(f"Written {filename}")

    for text, title in zip(bol_test, test_rins):
        filename = f"{title}.txt"
        with open(os.path.join('synth', 'data', 'e2e', 'test_template1', 'test',
                            'bol', filename), 'w') as file:
            file.write(text)
        print(f"Written {filename}")

    outcome = pd.read_csv(os.path.join('synth', 'data', 'edit', 'household_bus.csv'))
    outcome = outcome.\
        loc[outcome['DATE_STIRTHH'] == '1999-01-01']

    outcome_rins_1 = outcome['rinpersoon'].loc[outcome['EVENT'] == 'child_born']

    train_outcome = [rin in outcome_rins_1 for rin in train_rins]
    train_outcome_txt = ["1" if value else "0" for value in train_outcome]
    test_outcome = [rin in outcome_rins_1 for rin in test_rins]
    test_outcome_txt = ["1" if value else "0" for value in test_outcome]

    for text, title in zip(train_outcome_txt, train_rins):
        filename = f"{title}.txt"
        with open(os.path.join('synth', 'data', 'e2e', recipe, 'train',
                            'outcome', filename), 'w') as file:
            file.write(text)
        print(f"Written {filename}")

    for text, title in zip(train_outcome_txt, test_rins):
        filename = f"{title}.txt"
        with open(os.path.join('synth', 'data', 'e2e', recipe, 'test',
                            'outcome', filename), 'w') as file:
            file.write(text)
        print(f"Written {filename}")

