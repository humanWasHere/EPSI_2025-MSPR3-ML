from pathlib import Path
import pandas as pd

cleaned_data_path = Path(__file__).parents[1] / 'data' / 'cleaned_data'
merged_data_path = Path(__file__).parents[1] / 'data' / 'merged_data'

def merge_data() -> pd.DataFrame:
    """
    Merge the cleaned data from different sources into a single DataFrame.
    """
    
    # Load the cleaned data
    df_criminality = pd.read_csv(cleaned_data_path / 'criminalite' / 'criminalite_aura.csv', sep=';', encoding='utf-8-sig')
    df_defaillance = pd.read_csv(cleaned_data_path / 'defaillances_entreprises' / 'defaillances_entreprises_aura.csv', sep=';', encoding='utf-8-sig')
    df_chomage = pd.read_csv(cleaned_data_path / 'chomage' / 'chomage_aura.csv', sep=';', encoding='utf-8-sig')
    # df_pouvoir_achat = pd.read_csv(cleaned_data_path / 'pouvoir_achat' / 'pouvoir_achat_aura.csv', sep=';', encoding='utf-8-sig')

    # Merge the DataFrames on the 'Années' column
    merged_df = df_criminality.merge(df_defaillance, on='Années', how='outer').merge(df_chomage, on='Années', how='outer')  # .merge(df_pouvoir_achat, on='Années', how='outer')

    # Save the merged DataFrame
    merged_saving_path = merged_data_path / 'data_merged_aura.csv'
    merged_saving_path.parent.mkdir(parents=True, exist_ok=True)
    merged_df.to_csv(merged_saving_path, index=False, sep=';', encoding='utf-8-sig')

    print(f"Merged data saved to: {merged_saving_path}")
    
    return merged_df