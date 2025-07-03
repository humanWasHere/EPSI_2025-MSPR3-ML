from pathlib import Path
import pandas as pd

original_data_path = Path(__file__).parents[2] / 'data' / 'original_data'
cleaned_data_path = Path(__file__).parents[2] / 'data' / 'cleaned_data'

def get_pouvoir_achat() -> pd.DataFrame:
    return None

def get_criminality() -> pd.DataFrame:
    df = original_data_path / 'criminalite' / 'donnee-reg-data.gouv-2024-geographie2024-produit-le2025-03-14.csv'
    df_criminality = pd.read_csv(df, sep=';', encoding='utf-8')
    # Garder que les données pour la région Auvergne-Rhône-Alpes (Code_region = 84)
    df_criminality_aura = df_criminality[df_criminality['Code_region'] == 84]
    # Renommer les colonnes
    df_criminality_aura = df_criminality_aura.rename(columns={
        'annee': 'Année',
        'indicateur': 'Crimes',
        'taux_pour_mille': 'Taux de criminalité (pour mille)',
    })
    # Sélection des crimes à garder
    crimes_liste = [
        "Homicides",
        "Tentatives d'homicides",
        "Coups et blessures volontaires",
        "Coups et blessures volontaires intrafamiliaux",
        "Autres coups et blessures volontaires",
        "Violences sexuelles",
        "Vols avec armes",
        "Vols violents sans arme",
        "Vols sans violence contre des personnes",
        "Cambriolages de logement",
        "Vols de véhicules",
        "Vols dans les véhicules",
        # "Vols d'accessoires sur véhicules",
        "Destructions et dégradations volontaires",
        # "Usage de stupéfiants",
        # "Usage de stupéfiants (AFD)",
        "Trafic de stupéfiants",
        "Escroqueries"
    ]
    # Filtrer les crimes pour ne garder que ceux de la liste
    df_criminality_aura = df_criminality_aura[df_criminality_aura['Crimes'].isin(crimes_liste)]
    # Typing
    # Convertir 'Taux pour mille' en numérique, en remplaçant les virgules par des points
    df_criminality_aura['Taux de criminalité (pour mille)'] = df_criminality_aura['Taux de criminalité (pour mille)'].astype(str).str.replace(',', '.').astype(float)
    # Convertir 'Année' en entier
    df_criminality_aura['Année'] = df_criminality_aura['Année'].astype(int)
    # Supprimer les colonnes inutiles
    df_criminality_aura = df_criminality_aura.drop(columns=['Code_region', 'unite_de_compte', 'insee_pop_millesime', 'insee_log', 'insee_log_millesime'])
    # Special clean
    # Vérifier si 'Taux pour mille' est bien calculé comme 'nombre' * 1000 / 'insee_pop'
    calculated_taux = df_criminality_aura['nombre'] * 1000 / df_criminality_aura['insee_pop']
    invalid_mask = ~(calculated_taux.round(4) == df_criminality_aura['Taux de criminalité (pour mille)'].astype(float).round(4))
    if invalid_mask.any():
        print("Attention : certains taux pour mille ne correspondent pas au calcul attendu.")
        print(df_criminality_aura.loc[invalid_mask])
        # Supprimer les lignes invalides
        df_criminality_aura = df_criminality_aura.loc[~invalid_mask]
        df_criminality_aura = df_criminality_aura.reset_index(drop=True)
    # # Supprimer les colonnes inutiles
    # df_criminality_aura = df_criminality_aura.drop(columns=['Crimes', 'insee_pop', 'nombre'])
    df_grouped = df_criminality_aura.groupby('Année', as_index=False)['Taux de criminalité (pour mille)'].mean().round(3)
    criminalite_saving_path = cleaned_data_path / 'criminalite' / 'criminalite_aura.csv'
    criminalite_saving_path.parent.mkdir(parents=True, exist_ok=True)
    df_grouped.to_csv(criminalite_saving_path, index=False, sep=';', encoding='utf-8-sig')
    print(f"Le fichier des défaillances d'entreprises par année en AURA à été sauvegardé : {criminalite_saving_path}")
    return df_grouped

def get_defaillance_entreprise_by_year() -> pd.DataFrame:
    df = original_data_path / 'defaillance_entreprise' / 'valeurs_mensuelles.csv'
    df_defaillance = pd.read_csv(df, sep=';', encoding='utf-8')
    # Supprimer les lignes inutiles
    df_defaillance = df_defaillance.drop(df_defaillance.index[[0, 1, 2]])
    df_defaillance = df_defaillance.reset_index(drop=True)
    # Renommer les colonnes
    df_defaillance = df_defaillance.rename(columns={
        'Libellé': 'Mois',
        "Nombre de défaillances d'entreprises par date de jugement - Cumul brut glissant sur 12 mois - Auvergne-Rhône-Alpes - Tous secteurs d'activité": "Nombre de défaillances d'entreprises"
    })
    # Supprimer la colonne 'Codes'
    df_defaillance = df_defaillance.drop(columns=['Codes'])
    # Convertir 'Mois' en période Année-Mois sans jour
    df_defaillance['Mois'] = pd.to_datetime(df_defaillance['Mois'], format="%Y-%m", errors='coerce').dt.to_period('M')
    # typing
    df_defaillance['Année'] = df_defaillance['Mois'].dt.year.astype(int)
    df_defaillance["Nombre de défaillances d'entreprises"] = df_defaillance["Nombre de défaillances d'entreprises"].astype(int)
    df_defaillance = df_defaillance.drop(columns=['Mois'])  # Supprimer la colonne 'Mois' si nécessaire
    # Supprimer les lignes où l'année ou le nombre de défaillances est manquant
    df_defaillance = df_defaillance.dropna(subset=['Année', "Nombre de défaillances d'entreprises"])
    # Regrouper et sommer par année
    df_grouped = df_defaillance.groupby('Année', as_index=False).sum()
    defaillance_saving_path = cleaned_data_path / 'defaillances_entreprises' / 'defaillances_entreprises_aura.csv'
    defaillance_saving_path.parent.mkdir(parents=True, exist_ok=True)
    df_grouped.to_csv(defaillance_saving_path, index=False, sep=';', encoding='utf-8-sig')
    print(f"Le fichier des défaillances d'entreprises par année en AURA à été sauvegardé : {defaillance_saving_path}")
    return df_grouped

def get_chomage_by_year() -> pd.DataFrame:
    df = original_data_path / 'chomage' / 'valeurs_trimestrielles.csv'
    df_chomage = pd.read_csv(df, sep=';', encoding='utf-8')
    # Supprimer les lignes inutiles
    df_chomage = df_chomage.drop(df_chomage.index[[0, 1, 2]])
    df_chomage = df_chomage.rename(columns={
        'Libellé': 'Trimestre',
        "Taux de chômage localisé par région - Auvergne-Rhône-Alpes": "Taux de chômage"
    })
    # Convertir 'Trimestre' en période Trimestre sans jour
    # Typage
    df_chomage['Année'] = pd.PeriodIndex(df_chomage['Trimestre'].str.replace('T', 'Q'), freq='Q').year.astype(int)
    df_chomage['Taux de chômage'] = df_chomage['Taux de chômage'].astype(float)
    # Supprimer les colonnes 'Codes' et 'Trimestre'
    df_chomage = df_chomage.drop(columns=['Codes', 'Trimestre'])
    # Si besoin supprimer les lignes où l'année ou le taux de chomage est manquant
    df_chomage = df_chomage.dropna(subset=['Année', "Taux de chômage"])
    # Regrouper et sommer par année
    df_grouped = df_chomage.groupby('Année', as_index=False).mean()
    # Arrondir le taux de chômage à 2 décimales
    df_grouped['Taux de chômage'] = df_grouped['Taux de chômage'].round(3)
    chomage_saving_path = cleaned_data_path / 'chomage' / 'chomage_aura.csv'
    chomage_saving_path.parent.mkdir(parents=True, exist_ok=True)
    df_grouped.to_csv(chomage_saving_path, index=False, sep=';', encoding='utf-8-sig')
    print(f"Le fichier du taux de chomage par année en AURA à été sauvegardé : {chomage_saving_path}")

if __name__ == "__main__":
    # get_pouvoir_achat()
    get_criminality()
    get_defaillance_entreprise_by_year()
    get_chomage_by_year()
