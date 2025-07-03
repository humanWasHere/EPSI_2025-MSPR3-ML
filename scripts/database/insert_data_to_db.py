from pathlib import Path
import pandas as pd
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv(Path(__file__).parents[1] / '.env')

DB_NAME = os.getenv('DB_NAME')
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': int(os.getenv('DB_PORT'))
}

CSV_PATH = Path(__file__).parents[1] / 'data' / 'merged_data' / 'data_merged_by_year.csv'  # chemin relatif ou absolu

try:
    # Connexion à la base pour l'insertion
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_NAME,
        port=DB_CONFIG['port']
    )
    cursor = conn.cursor()
    print(f'Connexion à la base {DB_NAME} réussie.')

    # Vérification de la présence de la table
    cursor.execute("SHOW TABLES;")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Tables présentes dans la base : {tables}")
    if 'data_merged_by_year' not in tables:
        raise Exception("La table 'data_merged_by_year' n'existe pas dans la base. Veuillez la créer avant d'insérer des données.")

    # Lecture du CSV
    df = pd.read_csv(CSV_PATH)
    # Renommage des colonnes pour correspondre à la table SQL
    df = df.rename(columns={
        'Année': 'Annee',
        'Libellé du département': 'Libelle_departement',
        'Pourcentage tour 1': 'Pourcentage_tour_1',
        'Pourcentage tour 2': 'Pourcentage_tour_2',
        'Taux criminalite': 'Taux_criminalite',
        'Taux chomage': 'Taux_chomage',
        'Nombre defaillance entreprise': 'Nombre_defaillance_entreprise',
        'Gagnant tour 1': 'Gagnant_tour_1',
        'Gagnant tour 2': 'Gagnant_tour_2'
    })
    df = df.where(pd.notnull(df), None)

    insert_query = '''
        INSERT INTO data_merged_by_year (
            Annee, Libelle_departement, Candidat, Pourcentage_tour_1, Pourcentage_tour_2, Clivage,
            Taux_criminalite, Taux_chomage, Nombre_defaillance_entreprise, Gagnant_tour_1, Gagnant_tour_2
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    data = [
        (
            int(row['Annee']) if row['Annee'] is not None else None,
            str(row['Libelle_departement']) if row['Libelle_departement'] is not None else None,
            str(row['Candidat']) if row['Candidat'] is not None else None,
            float(row['Pourcentage_tour_1']) if row['Pourcentage_tour_1'] is not None else None,
            float(row['Pourcentage_tour_2']) if row['Pourcentage_tour_2'] is not None else None,
            str(row['Clivage']) if row['Clivage'] is not None else None,
            float(row['Taux_criminalite']) if row['Taux_criminalite'] is not None else None,
            float(row['Taux_chomage']) if row['Taux_chomage'] is not None else None,
            int(row['Nombre_defaillance_entreprise']) if row['Nombre_defaillance_entreprise'] is not None else None,
            int(row['Gagnant_tour_1']) if row['Gagnant_tour_1'] is not None else None,
            int(row['Gagnant_tour_2']) if row['Gagnant_tour_2'] is not None else None
        )
        for _, row in df.iterrows()
    ]
    cursor.executemany(insert_query, data)
    conn.commit()
    print(f"{cursor.rowcount} lignes insérées dans la table data_merged_by_year.")

except Error as e:
    print(f"Erreur MySQL : {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print('Connexion fermée.')
