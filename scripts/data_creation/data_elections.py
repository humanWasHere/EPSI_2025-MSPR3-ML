from pathlib import Path
import pandas as pd
import numpy as np

electorales_data_path = Path(__file__).parents[2] / 'data' / 'original_data' / 'electorales'
candidats_data_path = Path(__file__).parents[2] / 'data' / 'original_data' / 'candidats'
cleaned_data_path = Path(__file__).parents[2] / 'data' / 'cleaned_data'

yearListFile = {
    '1995.xls': 9,
    '2002.xls': 16,
    '2007.xls': 12,
    '2012.xls': 10,
    '2017.xls': 11,
    '2022.xls': 12
}
departments = ['AIN', 'ALLIER', 'ARDECHE', 'CANTAL', 'DROME', 'ISERE', 'LOIRE', 'HAUTE LOIRE', 'PUY DE DOME', 'RHONE', 'SAVOIE', 'HAUTE SAVOIE']  # Metropole de lyon
# dpt_nbs = [1, 3, 7, 15, 26, 38, 42, 43, 63, 69, 73, 74]  
df_results = pd.DataFrame()

def get_elections_results() -> pd.DataFrame:
    """
    Récupère les résultats des élections présidentielles en Auvergne-Rhône-Alpes.
    Les données sont extraites des fichiers Excel et filtrées par départements.
    Les résultats sont retournés sous forme de DataFrame.
    """

    df_results = pd.DataFrame()  # Initialisation locale

    for yearFile, num_candidates in yearListFile.items():
        dfT1 = pd.read_excel(electorales_data_path / yearFile, sheet_name='Départements T1')

        dfT1['Libellé du département'] = dfT1['Libellé du département'].str.replace('-', ' ').str.replace('ô', 'o').str.replace('è', 'e').str.upper()

        df = dfT1[dfT1['Libellé du département'].isin(departments)].copy()  # Copie explicite

        year = yearFile.split('.')[0]

        df['Année'] = year

        for i in range(0, num_candidates):
            columnVersion = ''
            if i > 0:
                columnVersion = '.' + str(i)

            df['Candidat'] = df['Prénom'+columnVersion] + ' ' + df['Nom'+columnVersion]
            df['Pourcentage tour 1'] = df['% Voix/Exp'+columnVersion]
            df['Pourcentage tour 2'] = 0.0  # Initialiser en float

            temp_df = df[['Année', 'Libellé du département', 'Candidat', 'Pourcentage tour 1', 'Pourcentage tour 2']].copy()

            df_results = pd.concat([df_results, temp_df], ignore_index=True)

        dfT2 = pd.read_excel(electorales_data_path / yearFile, sheet_name='Départements T2')
        dfT2['Libellé du département'] = dfT2['Libellé du département'].str.replace('-', ' ').str.replace('ô', 'o').replace('è', 'e').str.upper()
        dfT2 = dfT2[dfT2['Libellé du département'].isin(departments)].copy()  # Copie explicite

        for i in range(0, 2):
            columnVersion = ''
            if i > 0:
                columnVersion = '.' + str(i)

            for dep in departments:
                for idx, row in dfT2.iterrows():
                    candidat = row['Prénom'+columnVersion] + ' ' + row['Nom'+columnVersion]
                    if row['Libellé du département'] == dep and year in df_results['Année'].values and candidat in df_results['Candidat'].values:
                        value = row['% Voix/Exp'+columnVersion]
                        if isinstance(value, str):
                            value = float(value.replace(',', '.'))
                        df_results.loc[(df_results['Libellé du département'] == dep) & (df_results['Candidat'] == candidat) & (df_results['Année'] == year), 'Pourcentage tour 2'] = float(value)

    # S'assurer que la colonne est bien en float
    df_results['Pourcentage tour 2'] = df_results['Pourcentage tour 2'].astype(float)

    df_candidats = pd.read_excel(candidats_data_path / 'candidats.xlsx')

    df_results['Année'] = df_results['Année'].astype(str)
    df_candidats['Année'] = df_candidats['Année'].astype(str)

    df_results_by_candidats = pd.merge(df_results, df_candidats, how='left', on=['Année', 'Candidat'])

    return df_results_by_candidats
