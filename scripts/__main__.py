from data_creation.data_cleaning import get_criminality, get_defaillance_entreprise_by_year, get_chomage_by_year, get_pouvoir_achat
from data_creation.data_elections import get_elections_results
from data_creation.data_merging import merge_data

if __name__ == "__main__":
    # clean data
    get_criminality()
    get_defaillance_entreprise_by_year()
    get_chomage_by_year()
    # get_pouvoir_achat()
    # election data
    result = get_elections_results()
    # merge data
    merge_data(result)
