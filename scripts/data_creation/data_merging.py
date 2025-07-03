from pathlib import Path
import pandas as pd

cleaned_data_path = Path(__file__).parents[2] / 'data' / 'cleaned_data'
merged_data_path = Path(__file__).parents[2] / 'data' / 'merged_data'

# def merge_data() -> pd.DataFrame:
#     """
#     Merge the cleaned data from different sources into a single DataFrame.
#     """
    
#     # Load the cleaned data
#     df_criminality = pd.read_csv(cleaned_data_path / 'criminalite' / 'criminalite_aura.csv', sep=';', encoding='utf-8-sig')
#     df_defaillance = pd.read_csv(cleaned_data_path / 'defaillances_entreprises' / 'defaillances_entreprises_aura.csv', sep=';', encoding='utf-8-sig')
#     df_chomage = pd.read_csv(cleaned_data_path / 'chomage' / 'chomage_aura.csv', sep=';', encoding='utf-8-sig')
#     # df_pouvoir_achat = pd.read_csv(cleaned_data_path / 'pouvoir_achat' / 'pouvoir_achat_aura.csv', sep=';', encoding='utf-8-sig')

#     # Merge the DataFrames on the 'Année' column
#     merged_df = df_criminality.merge(df_defaillance, on='Année', how='outer').merge(df_chomage, on='Année', how='outer')  # .merge(df_pouvoir_achat, on='Année', how='outer')

#     # Save the merged DataFrame
#     merged_saving_path = merged_data_path / 'data_merged_aura.csv'
#     merged_saving_path.parent.mkdir(parents=True, exist_ok=True)
#     merged_df.to_csv(merged_saving_path, index=False, sep=';', encoding='utf-8-sig')

#     print(f"Merged data saved to: {merged_saving_path}")
    
#     return merged_df

def merge_data(df_results_by_candidats: pd.DataFrame) -> None:
    """
    Merge the election results with the cleaned data from different sources.
    """

    df_criminality = pd.read_csv(cleaned_data_path / 'criminalite' / 'criminalite_aura.csv', sep=';', encoding='utf-8-sig')
    df_defaillance = pd.read_csv(cleaned_data_path / 'defaillances_entreprises' / 'defaillances_entreprises_aura.csv', sep=';', encoding='utf-8-sig')
    df_chomage = pd.read_csv(cleaned_data_path / 'chomage' / 'chomage_aura.csv', sep=';', encoding='utf-8-sig')
    # df_pouvoir_achat = pd.read_csv(cleaned_data_path / 'pouvoir_achat' / 'pouvoir_achat_aura.csv', sep=';', encoding='utf-8-sig')

    yearsElection = df_results_by_candidats['Année'].unique()

    for i in range(len(yearsElection) - 1):
        start_year = int(yearsElection[i]) + 1
        end_year = int(yearsElection[i + 1])

        # # Pouvoir d'achat 
        # # Récupérer les taux de croissance annuels pour la période
        # achat_growth_rates = df_pouvoir_achat.loc[(df_pouvoir_achat['Annee'].astype(int) >= start_year) & 
        #                                     (df_pouvoir_achat['Annee'].astype(int) <= end_year), 'Pouvoir achat'].values
        # # Convertir les taux de croissance en multiplicateurs
        # achat_multipliers = [(rate / 100) + 1 for rate in achat_growth_rates]
        # # Calculer la croissance totale
        # achat_total_growth = np.prod(achat_multipliers)
        # # Convertir la croissance totale en un taux de croissance en pourcentage
        # achat_total_growth_rate = (achat_total_growth - 1) * 100
        # # Mettre à jour les lignes de df_results_by_candidats pour l'année actuelle avec la croissance totale
        # df_results_by_candidats.loc[df_results_by_candidats['Année'] == str(end_year), 'Pouvoir achat'] = achat_total_growth_rate

        # Criminalité 
        # Récupérer les taux de criminalité annuels pour la période
        crime_growth_rates = df_criminality.loc[(df_criminality['Année'].astype(int) >= start_year) & 
                                            (df_criminality['Année'].astype(int) <= end_year), 'Taux de criminalité (pour mille)'].values
        # Récupérer la moyenne durant le mandat 
        crime_average = 0
        if len(crime_growth_rates) > 0:
            crime_average = sum(crime_growth_rates) / len(crime_growth_rates)
        # Mettre à jour les lignes de df_results_by_candidats pour l'année actuelle avec le nombre de crime moyen
        df_results_by_candidats.loc[df_results_by_candidats['Année'] == str(end_year), 'Taux criminalite'] = crime_average

        # Chomage 
        # Récupérer les taux de chomage annuels pour la période
        chomage_growth_rates = df_chomage.loc[(df_chomage['Année'].astype(int) >= start_year) & 
                                            (df_chomage['Année'].astype(int) <= end_year), 'Taux de chômage'].values
        # Récupérer la moyenne durant le mandat 
        chomage_average = 0
        if len(chomage_growth_rates) > 0:
            chomage_average = sum(chomage_growth_rates) / len(chomage_growth_rates)
        # Mettre à jour les lignes de df_results_by_candidats pour l'année actuelle avec le nombre de chomage moyen
        df_results_by_candidats.loc[df_results_by_candidats['Année'] == str(end_year), 'Taux chomage'] = chomage_average

        # Défaillance d'entreprises 
        # Récupérer le nombre défaillances d'entreprises annuels pour la période
        defaillance_growth_rates = df_defaillance.loc[(df_defaillance['Année'].astype(int) >= start_year) & 
                                            (df_defaillance['Année'].astype(int) <= end_year), 'Nombre de défaillances d\'entreprises'].values
        # Récupérer la somme durant le mandat 
        defaillance_sum = 0
        if len(defaillance_growth_rates) > 0:
            defaillance_sum = sum(defaillance_growth_rates)
        # Mettre à jour les lignes de df_results_by_candidats pour l'annee actuelle avec le nombre de défaillance d'entreprise moyen
        df_results_by_candidats.loc[df_results_by_candidats['Année'] == str(end_year), 'Nombre defaillance entreprise'] = defaillance_sum

    df_results_by_candidats['Année'] = df_results_by_candidats['Année'].astype(int)
    df_results_by_candidats['Pourcentage tour 1'] = df_results_by_candidats['Pourcentage tour 1'].apply(lambda x: float(x.replace(',', '.')) if isinstance(x, str) and ',' in x else x)
    df_results_by_candidats['Pourcentage tour 2'] = df_results_by_candidats['Pourcentage tour 2'].apply(lambda x: float(x.replace(',', '.')) if isinstance(x, str) and ',' in x else x)
    # df_results_by_candidats['Pouvoir achat'] = df_results_by_candidats['Pouvoir achat'].astype(float)
    df_results_by_candidats['Taux criminalite'] = df_results_by_candidats['Taux criminalite'].astype(float)
    df_results_by_candidats['Taux chomage'] = df_results_by_candidats['Taux chomage'].astype(float).round(4)
    # Nettoyage pour éviter les erreurs de conversion
    import numpy as np
    for col in ['Taux criminalite', 'Taux chomage', 'Nombre defaillance entreprise']:
        df_results_by_candidats[col] = (
            df_results_by_candidats[col]
            .replace('', 0)
            .replace(' ', 0)
            .replace(np.nan, 0)
            .fillna(0)
            .astype(float)
        )
    df_results_by_candidats['Nombre defaillance entreprise'] = df_results_by_candidats['Nombre defaillance entreprise'].astype(int)


    # Obtenir les indices des lignes ayant le pourcentage le plus élevé pour chaque année et département
    idx1 = df_results_by_candidats.groupby(['Année', 'Libellé du département'])['Pourcentage tour 1'].idxmax()
    # Créer une nouvelle colonne 'Gagnant' et initialiser à 0
    df_results_by_candidats['Gagnant tour 1'] = 0
    # Mettre '1' dans la colonne 'Gagnant' pour les lignes correspondant aux indices obtenus
    df_results_by_candidats.loc[idx1, 'Gagnant tour 1'] = 1
    # Réinitialiser les index du DataFrame
    df_results_by_candidats = df_results_by_candidats.reset_index(drop=True)

    # Obtenir les indices des lignes ayant le pourcentage le plus élevé pour chaque année et département
    idx2 = df_results_by_candidats.groupby(['Année', 'Libellé du département'])['Pourcentage tour 2'].idxmax()
    # Créer une nouvelle colonne 'Gagnant' et initialiser à 0
    df_results_by_candidats['Gagnant tour 2'] = 0
    # Mettre '1' dans la colonne 'Gagnant' pour les lignes correspondant aux indices obtenus
    df_results_by_candidats.loc[idx2, 'Gagnant tour 2'] = 1
    # Réinitialiser les index du DataFrame
    df_results_by_candidats = df_results_by_candidats.reset_index(drop=True)

    df_results_by_candidats.to_excel(merged_data_path / 'data_merged_by_year.xlsx', index=False)
    df_results_by_candidats.to_csv(merged_data_path / 'data_merged_by_year.csv', index=False)
    print(f"Les résultats des élections ont été fusionnés et sauvegardés dans : {merged_data_path / 'data_merged_by_year.csv'}")
    print(f"Les résultats des élections ont été fusionnés et sauvegardés dans : {merged_data_path / 'data_merged_by_year.xlsx'}")
