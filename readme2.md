Étape 1 : Migration des Données Médicales vers MongoDB
Ce module gère le prétraitement, le contrôle d'intégrité, le typage et le transfert automatisé du dataset médical (healthcare_dataset.csv) vers une instance MongoDB locale.
📂 Structure du Projet (Étape 1)
Plaintext
medical-migration-project/
│
├── healthcare_dataset.csv     # Dataset source des patients (55 500 lignes)
├── migrate.py                 # Script principal d'automatisation de la migration
├── test_pipeline.py           # Tests unitaires et d'intégrité automatisés (pytest)
├── requirements.txt           # Dépendances et versions des modules Python
└── README.md                  # Documentation de l'Étape 1
⚙️ Prérequis & Installation
Python (version 3.10 ou supérieure recommandée)
Docker Desktop (pour exécuter MongoDB en local)
1. Lancer MongoDB via Docker
Dans votre terminal, lancez un conteneur MongoDB local sur le port par défaut (27017) :
Bash
docker run -d --name mongodb-local -p 27017:27017 mongo:latest
2. Configurer l'environnement virtuel Python
Bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel (sur macOS / Linux)
source venv/bin/activate

# Installer les dépendances requises
pip install -r requirements.txt
🔄 Logique de la Migration (migrate.py)
Le script de migration exécute les étapes suivantes de manière séquentielle et sécurisée :
Chargement et Exploration : Lecture du fichier CSV source (healthcare_dataset.csv) via la bibliothèque pandas.
Nettoyage et Typage :
Suppression des espaces superflus dans les en-têtes de colonnes.
Conversion explicite des types (variables numériques pour l'âge et les montants de facturation, types temporels pour les dates d'admission et de sortie).
Normalisation des valeurs manquantes (NaN) en None pour garantir une compatibilité parfaite avec le format BSON de MongoDB.
Indexation Stratégique : Création d'index sur les champs clés (Medical Condition, Age) afin d'optimiser les performances des futures requêtes de recherche médicale.
Insertion par Lots (Bulk Insert) : Transfert des données par blocs (par lots de 10 000 documents) pour optimiser l'utilisation de la mémoire et accélérer l'insertion des 55 500 enregistrements.
Comment lancer la migration ?
Bash
python migrate.py
🧪 Automatisation des Tests d'Intégrité (test_pipeline.py)
Un ensemble de tests automatisés est mis en place via pytest pour s'assurer de la qualité et de la cohérence des données avant et après le transfert.
Ce que vérifient les tests :
Présence et structure du CSV : Vérifie que le fichier source existe et contient les colonnes obligatoires.
Connexion MongoDB : Valide que le serveur MongoDB répond correctement.
Intégrité volumétrique : Compare le nombre exact de lignes du fichier CSV source avec le nombre de documents insérés dans la collection MongoDB.
Format des documents : S'assure que les documents stockés possèdent un identifiant unique _id valide.
Lancer les tests :
Bash
pytest -v
📦 Import et Export des Données (Sauvegarde)
Pour sauvegarder ou restaurer rapidement vos collections hors script Python :
Exporter la base de données au format archive binaire :
Bash
docker exec -t mongodb-local mongodump --db=medical_db --archive=/tmp/medical_backup.archive
docker cp mongodb-local:/tmp/medical_backup.archive ./medical_backup.archive
Restaurer la base de données :
Bash
docker cp ./medical_backup.archive mongodb-local:/tmp/medical_backup.archive
docker exec -t mongodb-local mongorestore --db=medical_db --archive=/tmp/medical_backup.archive --drop