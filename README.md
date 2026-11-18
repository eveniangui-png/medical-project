# 🏥 Projet de Data Engineering : Migration de Données Médicales vers MongoDB (Docker & AWS)

## 📌 1. Contexte et Objectifs du Projet

Dans le cadre de la modernisation du système d'information de santé d'un client, ce projet vise à migrer un dataset volumineux de données patients (`healthcare_dataset.csv`, comprenant **55 500 enregistrements**) depuis un stockage plat (CSV) vers une base de données NoSQL distribuée (**MongoDB**).

### Objectifs principaux :
- **Flexibilité du schéma :** Modéliser les données médicales sous forme de documents JSON/BSON avec typage strict (dates ISO, montants numériques) pour faciliter l'évolution future des attributs de santé.
- **Conteneurisation complète :** Déployer un environnement reproductible et isolé via **Docker** (`Dockerfile` dédié pour l'application Python et `docker-compose.yml` pour orchestrer l'application et MongoDB).
- **Optimisation & Qualité :** Automatiser le pipeline ETL via un script Python (`migrate.py`) utilisant l'insertion par lots (*Bulk Insert* de 10 000 documents) et valider l'intégrité globale avec une suite de tests (`pytest`).
- **Préparation au Cloud (AWS) :** Concevoir l'architecture cible scalable sur **AWS** (Amazon S3, Amazon DocumentDB, AWS Fargate).

---

## 🗂️ 2. Structure Complète du Projet

```text
medical-project/
│
├── .gitignore                 # Fichiers et dossiers ignorés par Git (venv/, __pycache__/, .DS_Store)
├── Dockerfile                 # Image Docker légère (python:3.11-slim) pour le script de migration
├── docker-compose.yml         # Orchestration multi-conteneurs (MongoDB + Application ETL)
├── healthcare_dataset.csv     # Dataset source (55 500 lignes, 15 attributs)
├── migrate.py                 # Pipeline ETL principal : nettoyage, typage et insertion par lots (Pandas/PyMongo)
├── test_migration.py          # Suite de tests d'intégrité automatisée (Pytest)
├── requirements.txt           # Liste des dépendances Python (pandas, pymongo, pytest)
└── README.md                  # Documentation technique détaillée du projet


  ##  🛠️ 3. Technologies et Stack Technique
Langage de programmation : Python 3.11
Traitement & Nettoyage de données : pandas (nettoyage des colonnes, typage numérique/dates, conversion BSON)
Pilote MongoDB : pymongo (insertion par lots insert_many et indexation B-Tree)
Conteneurisation : Docker Desktop, Dockerfile, Docker Compose
Tests unitaires & Intégrité : pytest
Base de données NoSQL : MongoDB (Local), Amazon DocumentDB (Cible Cloud AWS)

###🚀 4. Guide d'Installation et d'Exécution Pas-à-Pas
Prérequis Système
Docker Desktop installé et démarré.
(Optionnel pour exécution locale) Python 3.10+ et pip configurés.
Option A : Exécution 100 % Conteneurisée via Docker Compose (Recommandé)
Se placer dans le dossier du projet :
Bash
cd ~/Desktop/medical-project
Construire l'image et lancer l'infrastructure complète (MongoDB + Pipeline ETL) :
Bash
docker compose up --build
Docker va automatiquement démarrer le conteneur mongodb-local, construire l'image de migration-app via le Dockerfile, et exécuter la migration de bout en bout.
Option B : Exécution Locale via Environnement Virtuel (venv)
Initialiser et activer l'environnement virtuel Python :
Bash
python3 -m venv venv
source venv/bin/activate
Installer les dépendances nécessaires :
Bash
pip install -r requirements.txt
Démarrer uniquement la base de données MongoDB :
Bash
docker compose up -d mongodb
Exécuter le pipeline de migration des données :
Bash
python migrate.py
Résultat attendu dans la console :
Plaintext
============================================================
🚀 DÉBUT DE LA MIGRATION VERS MONGODB
============================================================
📖 Chargement du fichier CSV : healthcare_dataset.csv...
-> 55500 lignes chargées depuis le CSV.
🧹 Nettoyage et typage des données en cours...
🔌 Connexion à MongoDB (mongodb://localhost:27017/)...
⚙️ Création des index (Medical Condition, Age)...
🗑️ Nettoyage de la collection 'patients' avant insertion...
📥 Insertion des données par lots de 10000 documents...
   -> 10000 / 55500 documents insérés...
   -> 20000 / 55500 documents insérés...
   -> 30000 / 55500 documents insérés...
   -> 40000 / 55500 documents insérés...
   -> 50000 / 55500 documents insérés...
   -> 55500 / 55500 documents insérés...
============================================================
✅ MIGRATION TERMINÉE AVEC SUCCÈS !
📊 Total de documents dans MongoDB : 55500
============================================================
Étape de Validation : Lancer la suite d'assurance qualité (pytest)
Bash
pytest test_migration.py
🔍 5. Conception et Modélisation NoSQL
🔍 5. Conception et Modélisation NoSQL
Structure des Données (medical_db / patients)
Chaque ligne du CSV original est nettoyée, typée (conversion des dates et valeurs numériques, gestion des valeurs nulles NaN vers None) et convertie en un document JSON/BSON structuré au format suivant :
JSON
{
  "_id": ObjectId("654321abcdef1234567890ab"),
  "Name": "Bobby Jackson",
  "Age": 42,
  "Gender": "Male",
  "Blood Type": "B+",
  "Medical Condition": "Cancer",
  "Date of Admission": ISODate("2024-01-15T00:00:00Z"),
  "Doctor": "Matthew Smith",
  "Hospital": "Sons and Daughters Hospital",
  "Insurance Provider": "Blue Cross",
  "Billing Amount": 18856.27,
  "Room Number": 302,
  "Admission Type": "Emergency",
  "Discharge Date": ISODate("2024-02-02T00:00:00Z"),
  "Medication": "Paracetamol",
  "Test Results": "Normal"
}
Stratégie d'Indexation et Performance
Optimisation mémoire : Insertion par lots (chunks) de 10 000 documents (BATCH_SIZE = 10000) via insert_many().
Indexation B-Tree : Pour accélérer les requêtes analytiques et filtrages médicaux fréquents, des index ascendants ont été configurés sur les champs Medical Condition et Age :
Python
collection.create_indexes([
    IndexModel([("Medical Condition", ASCENDING)]),
    IndexModel([("Age", ASCENDING)])
])
🧪 6. Plan d'Assurance Qualité & Tests d'Intégrité (test_migration.py)
La validation du pipeline repose sur 3 tests automatisés exécutés avec Pytest :
test_mongo_connection : Établit un ping d'administration pour confirmer la réactivité du service MongoDB.
test_document_count : Compare dynamiquement le nombre de lignes du fichier CSV source (
N
=
55
 
500
N=55 500) avec le nombre de documents comptabilisés dans la collection patients.
test_sample_document_integrity : Valide le schéma d'un document échantillon en vérifiant la présence et la conformité des champs critiques (Name, Medical Condition, Billing Amount).
☁️ 7. Architecture Cible & Stratégie Cloud (AWS)
Pour répondre aux enjeux de montée en charge, de haute disponibilité et de sécurité des données de santé (HDS / HIPAA), l'infrastructure conteneurisée est prête à être déployée sur le Cloud AWS :
Plaintext
[ Fichier CSV ] ──> [ Amazon S3 ] ──> [ AWS Fargate (ECS) ] ──> [ Amazon DocumentDB ]
 (Source Brute)     (Bucket Privé)     (Conteneur Docker)       (Cluster NoSQL Multi-AZ)
Composant Cible AWS	Rôle et Justification Technique
Amazon S3	Stockage sécurisé (KMS SSE-S3), durable (99,999999999%) et économique des fichiers CSV sources.
Amazon DocumentDB	Base NoSQL distribuée fully-managed compatible MongoDB. Gestion automatique des sauvegardes, réplication multi-AZ et scalabilité horizontale.
AWS Fargate (ECS)	Exécution serverless de l'image Docker construite via notre Dockerfile sans gestion ni maintenance des instances sous-jacentes.
AWS KMS & IAM	Gestion fine des accès (Moindre Privilège) et chiffrement systématique des données au repos et en transit (TLS/SSL).
📝 8. Journal de Bord & Suivi de Projet
[x] Initialisation du repository (medical-project), configuration de .gitignore et de l'environnement virtuel (venv).
[x] Conteneurisation complète via Dockerfile et orchestration multi-services via docker-compose.yml.
[x] Écriture et optimisation du script ETL migrate.py (nettoyage, typage, indexation et insertion par lots de 55 500 documents).
[x] Développement de la suite de tests automatisée test_migration.py (pytest).
[x] Validation des critères d'intégrité de données.
[x] Conception du dossier d'architecture pour le déploiement sur AWS.