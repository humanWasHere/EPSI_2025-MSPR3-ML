import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Chargement des données
DATA_PATH = Path(__file__).parents[1] / 'data' / 'merged_data' / 'data_merged_by_year.csv'
df = pd.read_csv(DATA_PATH)

# Renommage pour faciliter l'accès
col_rename = {
    'Année': 'Annee',
    'Libellé du département': 'Libelle_departement',
    'Pourcentage tour 1': 'Pourcentage_tour_1',
    'Pourcentage tour 2': 'Pourcentage_tour_2',
    'Taux criminalite': 'Taux_criminalite',
    'Taux chomage': 'Taux_chomage',
    'Nombre defaillance entreprise': 'Nombre_defaillance_entreprise',
    'Gagnant tour 1': 'Gagnant_tour_1',
    'Gagnant tour 2': 'Gagnant_tour_2'
}
df = df.rename(columns=col_rename)

# 1. Distribution des taux de criminalité par année
plt.figure(figsize=(10,6))
sns.boxplot(x='Annee', y='Taux_criminalite', data=df)
plt.title('Distribution du taux de criminalité par année')
plt.ylabel('Taux de criminalité')
plt.xlabel('Année')
plt.tight_layout()
plt.savefig('criminalite_par_annee.png')
plt.close()

# 2. Taux de chômage moyen par année
plt.figure(figsize=(10,6))
sns.barplot(x='Annee', y='Taux_chomage', data=df, ci=None, estimator='mean')
plt.title('Taux de chômage moyen par année')
plt.ylabel('Taux de chômage moyen')
plt.xlabel('Année')
plt.tight_layout()
plt.savefig('chomage_moyen_par_annee.png')
plt.close()

# 3. Nombre de défaillances d'entreprise par département (top 10)
defaillances = df.groupby('Libelle_departement')['Nombre_defaillance_entreprise'].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,6))
defaillances.plot(kind='bar', color='orange')
plt.title('Top 10 départements par nombre moyen de défaillances d\'entreprise')
plt.ylabel('Nombre moyen de défaillances')
plt.xlabel('Département')
plt.tight_layout()
plt.savefig('defaillances_top10.png')
plt.close()

# 4. Répartition des clivages politiques
plt.figure(figsize=(8,6))
df['Clivage'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
plt.title('Répartition des clivages politiques')
plt.ylabel('')
plt.tight_layout()
plt.savefig('clivages_pie.png')
plt.close()

# 5. Corrélation entre variables numériques
plt.figure(figsize=(10,8))
sns.heatmap(df[[
    'Pourcentage_tour_1', 'Pourcentage_tour_2', 'Taux_criminalite', 'Taux_chomage', 'Nombre_defaillance_entreprise'
]].corr(), annot=True, cmap='coolwarm')
plt.title('Corrélation entre variables numériques')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')
plt.close()

print('Graphiques générés :')
print('- criminalite_par_annee.png')
print('- chomage_moyen_par_annee.png')
print('- defaillances_top10.png')
print('- clivages_pie.png')
print('- correlation_heatmap.png')
