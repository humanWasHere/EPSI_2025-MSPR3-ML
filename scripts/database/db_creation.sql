-- Script de création de la base de données et de la table pour les données électorales
DROP DATABASE IF EXISTS MSPR3_ML_elections;
CREATE DATABASE IF NOT EXISTS MSPR3_ML_elections;
USE MSPR3_ML_elections;

-- Table principale pour les données fusionnées
CREATE TABLE IF NOT EXISTS data_merged_by_year (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Annee INT NOT NULL,
    Libelle_departement VARCHAR(64) NOT NULL,
    Candidat VARCHAR(64) NOT NULL,
    Pourcentage_tour_1 FLOAT,
    Pourcentage_tour_2 FLOAT,
    Clivage VARCHAR(32),
    Taux_criminalite FLOAT,
    Taux_chomage FLOAT,
    Nombre_defaillance_entreprise INT,
    Gagnant_tour_1 INT,
    Gagnant_tour_2 INT
);
