# MSPR3

Nous avons choisi de nous concentrer sur la région Auvergne Rhône Alpes (AURA - 84).
Tout nos datasets sont issus des sites data.gouv ou inssee.fr.

Sommaire :
1. [TL;DR - lancement de l'app](#tl;dr---lancement-de-l'app-)
2. [Liens des datasets - Auvergne Rhône Alpes](#liens-des-datasets---auvergne-rhône-alpes-)
3. [Architecture du dépôt de code](#architecture-du-dépôt-de-code-)
4. [Collaborateurs](#collaborateurs-)

## TL;DR - lancement de l'app
En premier lieu, faites en sorte d'avoir un environnement python valide avec toutes les dépendances de librairies installées.
Dans le dossier root du projet clonné, lancer la commande suivante.
```csh
python ./scripts/__main__.py
```
Cela va créer les datasets nettoyés et les assembler afin de pouvoir les utiliser pour de l'entrainement et du teste de modèle de ML.  
Une fois cela fait, utiliser le fichier `./scripts/machine_learning.ipynb` pour utiliser les modèles de ML.

## Liens des datasets - Auvergne Rhône Alpes
L'ensemble des datasets d'origine est répartie dans le dossier   
Numéro de région officiel : 84

### Datasets d'élections
- élections de 2022 : https://www.data.gouv.fr/en/datasets/r/cb0bd397-c135-4540-b92e-e536ad4dbc8e

### Informations complémentaires
- taux de chomage : https://www.insee.fr/fr/statistiques/serie/001739986#Telechargement
- taux de criminalité (2 fichiers de base statistiques régionnales) : https://www.data.gouv.fr/fr/datasets/bases-statistiques-communale-departementale-et-regionale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/
- défaillance des entreprises : https://www.insee.fr/fr/statistiques/serie/001740154#Telechargement
- pouvoir d'achat : 

### Pour aller plus loin...
- taux d'inégalité : https://www.insee.fr/fr/outil-interactif/5367857/territoires/30_RPC/31_RNP#

## Architecture du dépôt de code
Cette arborescence est complète une fois le script lancé (génération automatique des dossiers clean + merge)  
```
.
├── .gitignore
├── README.md
├── scripts-app/
│   ├── data_cleaning.py
│   ├── data_election.py
│   ├── data_merging.py
│   └── machine_learning_model.ipynb
└── data-assets/
    ├── original_data/
    │   ├── chomage/
    │   │   └── 
    │   ├── criminalite/
    │   │   └── 
    │   └── defaillances_entreprises/
    │       └── 
    ├── cleaned_data/
    │   ├── chomage/
    │   │   └── 
    │   ├── criminalite/
    │   │   └── 
    │   └── defaillances_entreprises/
    │       └── 
    └── merged_data/
        └── data_merged.csv
```

## Collaborateurs
- CHANELIERE Romain
- CASELLA Théo
- BOUKHEMIRI Rafik