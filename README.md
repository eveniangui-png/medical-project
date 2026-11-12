# 🏥 Projet de Data Engineering : Migration de Données Médicales vers MongoDB (Docker & AWS)

## 📌 1. Contexte et Objectifs du Projet

Dans le cadre de la modernisation du système d'information de santé d'un client, ce projet vise à migrer un dataset volumineux de données patients (`healthcare_dataset.csv`, comprenant **55 500 enregistrements**) depuis un stockage plat (CSV) vers une base de données NoSQL distribuée (**MongoDB**).

### Objectifs principaux :
- **Flexibilité du schéma :** Modéliser les données médicales sous forme de documents JSON/BSON pour faciliter l'évolution future des attributs de santé.
- **Conteneurisation locale :** Déployer un environnement de développement reproductible et isolé via **Docker Desktop** et `docker-compose`.
- **Automatisation & Qualité :** Automatiser le pipeline d'ingestion via un script Python dédié (`migrate.py`) et valider l'intégrité globale avec une suite de tests unitaires et d'intégration (`pytest`).
- **Préparation au Cloud (AWS) :** Concevoir l'architecture cible scalable sur **AWS** (Amazon S3, Amazon DocumentDB, AWS Fargate).

---

## 🗂️ 2. Structure Complète du Projet

```text
medical-migration-project/
│
├── venv/                      # Environnement virtuel Python 3 (isolé)
├── docker-compose.yml         # Fichier d'orchestration Docker pour MongoDB 7.0
├── healthcare_dataset.csv     # Dataset source (55 500 lignes, 15 attributs)
├── migrate.py                 # Script principal d'ingestion et de transformation (Pandas/PyMongo)
├── test_migration.py          # Suite de tests d'intégrité automatisée (Pytest)
├── requirements.txt           # Liste des dépendances Python et versions verrouillées
└── README.md                  # Documentation technique détaillée du projet
```

---

## 🛠️ 3. Technologies et Stack Technique

- **Langage de programmation :** Python 3.x
- **Traitement de données :** `pandas` (lecture CSV et conversion BSON)
- **Pilote MongoDB :** `pymongo`
- **Conteneurisation :** Docker Desktop, Docker Compose (Image officielle `mongo:7.0`)
- **Tests unitaires & Intégrité :** `pytest`
- **Base de données NoSQL :** MongoDB 7.0 (Local), Amazon DocumentDB (Cible Cloud AWS)

---

## 🚀 4. Guide d'Installation et d'Exécution Pas-à-Pas

### Prérequis Système
- **Docker Desktop** installé et démarré.
- **Python 3.10+** et `pip` configurés.

### Étape 1 : Cloner / Se placer dans le dossier du projet
```bash
cd ~/Desktop/medical-migration-project
```

### Étape 2 : Initialiser et activer l'environnement virtuel Python
```bash
python3 -m venv venv
source venv/bin/activate
```

### Étape 3 : Installer les dépendances nécessaires
```bash
pip install -r requirements.txt
```

### Étape 4 : Déployer l'infrastructure locale MongoDB via Docker
```bash
docker compose up -d
```
*Pour vérifier que le conteneur tourne correctement :*
```bash
docker ps
```
*(Le conteneur `medical_mongo_db` doit afficher le statut `Up` sur le port `27017`).*

### Étape 5 : Exécuter le pipeline de migration des données
```bash
python migrate.py
```
*Résultat attendu dans la console :*
```text
--- Début de la migration depuis healthcare_dataset.csv ---
Connexion à MongoDB réussie !
Index créé sur la colonne 'Name'.
Fichier chargé avec succès : 55500 lignes trouvées.
Insertion des données en cours dans MongoDB...
Succès ! 55500 documents insérés dans la collection 'patients'.
```

### Étape 6 : Lancer la suite d'assurance qualité et d'intégrité
```bash
pytest test_migration.py
```

---

## 🔍 5. Conception et Modélisation NoSQL

### Structure des Données (`medical_db` / `patients`)
Chaque ligne du CSV original est convertie en un document JSON/BSON structuré au format suivant :

```json
{
  "_id": ObjectId("654321abcdef1234567890ab"),
  "Name": "Bobby Jackson",
  "Age": 42,
  "Gender": "Male",
  "Blood Type": "B+",
  "Medical Condition": "Cancer",
  "Date of Admission": "2024-01-15",
  "Doctor": "Matthew Smith",
  "Hospital": "Sons and Daughters Hospital",
  "Insurance Provider": "Blue Cross",
  "Billing Amount": 18856.27,
  "Room Number": 302,
  "Admission Type": "Emergency",
  "Discharge Date": "2024-02-02",
  "Medication": "Paracetamol",
  "Test Results": "Normal"
}
```

### Stratégie d'Indexation
Pour garantir des requêtes ultra-performantes lors de la recherche des dossiers patients par nom, un index B-Tree a été configuré sur le champ `Name` :
```python
collection.create_index("Name")
```

---

## 🧪 6. Plan d'Assurance Qualité & Tests d'Intégrité (`test_migration.py`)

La validation du pipeline repose sur 3 tests automatisés exécutés avec Pytest :

1. **`test_mongo_connection` :** Établit un ping d'administration pour confirmer la réactivité du service MongoDB.
2. **`test_document_count` :** Compare dynamiquement le nombre de lignes du fichier CSV source ($N = 55\ 500$) avec le nombre de documents comptabilisés dans la collection `patients`.
3. **`test_sample_document_integrity` :** Valide le schéma d'un document échantillon en vérifiant la présence et la conformité des champs critiques (`Name`, `Medical Condition`, `Billing Amount`).

---

## ☁️ 7. Architecture Cible & Stratégie Cloud (AWS)

Pour répondre aux enjeux de montée en charge, de haute disponibilité et de sécurité des données de santé (HDS / HIPAA), l'infrastructure est prête à être migrée sur le Cloud **AWS** :

```text
[ Fichier CSV ] ──> [ Amazon S3 ] ──> [ AWS Fargate (ECS) ] ──> [ Amazon DocumentDB ]
 (Source Brute)     (Bucket Privé)     (Task Ingestion)        (Cluster NoSQL Multi-AZ)
```

| Composant Cible AWS | Rôle et Justification Technique |
| :--- | :--- |
| **Amazon S3** | Stockage sécurisé (KMS SSE-S3), durable (99,999999999%) et économique des fichiers CSV sources. |
| **Amazon DocumentDB** | Base NoSQL distribuée fully-managed compatible MongoDB. Gestion automatique des sauvegardes, réplication multi-AZ et scalabilité horizontale. |
| **AWS Fargate (ECS)** | Exécution conteneurisée et *serverless* du script `migrate.py` sans gestion ni maintenance des instances sous-jacentes. |
| **AWS KMS & IAM** | Gestion fine des accès (Moindre Privilège) et chiffrement systématique des données au repos et en transit (TLS/SSL). |

---

## 📝 8. Journal de Bord & Suivi de Projet

- [x] Initialisation du repository et de l'environnement virtuel (`venv`).
- [x] Orchestration du conteneur MongoDB via `docker-compose.yml`.
- [x] Écriture et optimisation du script de migration `migrate.py` (55 500 documents insérés).
- [x] Développement de la suite de tests automatisée `test_migration.py` (`pytest`).
- [x] Validation des critères d'intégrité de données.
- [x] Conception du dossier d'architecture pour le passage sur AWS.

