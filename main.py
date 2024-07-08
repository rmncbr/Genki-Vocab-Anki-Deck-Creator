import random
import pandas as pd
import genanki

# For automatic creation of Genki Anki card decks, with acknowledgement to the folks at ohelo.org
# When it's time to create a new deck after a lesson, update names for Model, Deck, Save File, and Source URL.
# Genki Lessons 1 and 2 include Romaji translations for vocab.
# There is void of a Romaji field for the Anki card template.
# As such, you will have to update the deck creation to satisfy specific columns in the dataframe.
def create_anki_deck(dataframe):
    # Creating the model
    model_id = random.randrange(1 << 30, 1 << 31)       # random id for model
    print("Model ID: ", model_id)

    my_model = genanki.Model(
        model_id,
        'Genki 1 Lesson 7',             # model name to update
        fields=[
            {'name': 'Front'},
            {'name': 'Back'},
            {'name': 'Kanji'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '<br><br><div style=\'font-family: BIZ UDGothic; font-size: 24px; text-align: center;\'>{{Front}}</div><br><div style=\'font-family: BIZ UDGothic; font-size: 48px; text-align: center;\'>{{Kanji}}</div>',
                'afmt': '<br><br><div style=\'font-family: BIZ UDGothic; font-size: 24px; text-align: center;\'>{{Front}}</div><br><div style=\'font-family: BIZ UDGothic; font-size: 48px; text-align: center;\'>{{Kanji}}</div><hr id="answer" style="text-align: center;"><div style=\'font-family: Arial, sans-serif; font-size: 24px; text-align: center;\'>{{Back}}</div>',
            },
        ])

    deck_id = random.randrange(1 << 30, 1 << 31)                # random id for deck
    print("Deck ID: ", deck_id)

    my_deck = genanki.Deck(deck_id, "Genki 1 Lesson 7")         # deck name to update
    for column_name, column_data in dataframe.items():                 # traverse columns in dataframe, scrape each element per column
        if column_name == 0:                                            # col 0 scrapes kana
            kana_values = list(column_data[1:])
        elif column_name == 1:                                          # col 1 scrapes kanji (if listed)
            kanji_values = list(column_data[1:])
        elif column_name == 2:                                          # col 2 scrapes english translation
            english_translation_values = list(column_data[1:])
        # elif column_name == 3:                                          # col 3 scrapes english translation (Lessons 1 & 2)
        #     english_translation_values = list(column_data[1:])

    for kana, kanji, english in zip(kana_values, kanji_values, english_translation_values):         # assign string values to card notes
        my_note = genanki.Note(
            model=my_model,
            fields=[str(kana), str(english), str(kanji)]
        )
        my_deck.add_note(my_note)

    genanki.Package(my_deck).write_to_file('g1_l7.apkg')            # save file to update

def scrapeth():
    base_url = 'http://ohelo.org/japn/lang/genki_vocab_table.php?lesson=7'      # web lesson to update (lesson={1-23})
    table = pd.read_html(base_url)
    # Choose the correct DataFrame
    df = table[0]
    df.fillna('', inplace=True)
    # print(df)

    # Create Anki deck and cards
    create_anki_deck(df)


# Call the function to execute the script
scrapeth()
