from pathlib import Path
import pandas as pd

original_data_path = Path(__file__).parents[1] / 'data' / 'original_data'
cleaned_data_path = Path(__file__).parents[1] / 'data' / 'cleaned_data'

# FIXME DRAFT

# def get_elections() -> pd.DataFrame:
#     """
#     Récupère les données des élections en Auvergne-Rhône-Alpes et les nettoie.
#     Les données sont lues depuis un fichier CSV, nettoyées, et sauvegardées dans un nouveau fichier CSV.
#     """

    # 

    # df = original_data_path / 'elections' / 'elections_aura.csv'
    # df_elections = pd.read_csv(df, sep=';', encoding='utf-8')

    # # Renommer les colonnes
    # df_elections = df_elections.rename(columns={
    #     'annee': 'Années',
    #     'type_election': 'Type d\'élection',
    #     'resultat': 'Résultat'
    # })

    # # Convertir 'Années' en entier
    # df_elections['Années'] = df_elections['Années'].astype(int)

    # # Supprimer les lignes où l'année ou