from CSVCleaner import CSVCleaner


cleaner = CSVCleaner(r'data\raw\12k_VERIFIED_RAW.csv')



cleaner.read_csv()
cleaner.read_dict('dictionaries/french_english_dictionary.json')

# Normalize the column headings
cleaner.normalize_column_headings()



cleaner.write_column_to_txt('city', 'logs/city.txt')

print(cleaner.df['city'])

cleaner.read_filter('dictionaries/Filter.json')



## Filter out non-French speaking regions
# cleaner.remove_non_french_speaking_regions('state')



## Translate the columns
cleaner.translate_column('city')
cleaner.translate_column('state')
cleaner.translate_column('country')
cleaner.translate_column('company_city')





cleaner.write_column_to_txt('city', 'logs/state_after.txt')






cleaner.write('data/clean/12k_VERIFIED_CLEAN.csv')
