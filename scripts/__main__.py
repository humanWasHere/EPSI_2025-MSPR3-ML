from data_cleaning import get_criminality, get_defaillance_entreprise_by_year, get_chomage_by_year, get_pouvoir_achat
from data_merging import merge_data

if __name__ == "__main__":
    # clean data
    get_criminality()
    get_defaillance_entreprise_by_year()
    get_chomage_by_year()
    get_pouvoir_achat()
    # merge data
    merge_data()
