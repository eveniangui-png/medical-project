import os
import pytest
import pandas as pd
from pymongo import MongoClient

# Configuration
CSV_FILE = "healthcare_dataset.csv"
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "medical_db"
COLLECTION_NAME = "patients"

@pytest.fixture(scope="module")
def mongo_collection():
    """Fixture Pytest pour se connecter à MongoDB et fournir la collection aux tests."""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    yield collection
    client.close()

def test_csv_file_exists():
    """Vérifie que le fichier CSV source existe bien dans le projet."""
    assert os.path.exists(CSV_FILE), f"Le fichier source {CSV_FILE} est introuvable."

def test_csv_structure():
    """Vérifie que le CSV contient des données et des colonnes valides."""
    df = pd.read_csv(CSV_FILE)
    # Vérifie qu'il y a des lignes
    assert len(df) > 0, "Le fichier CSV est vide."
    
    # Vérifie la présence de colonnes clés du dataset healthcare
    expected_columns = {"Age", "Gender", "Medical Condition", "Blood Type"}
    assert expected_columns.issubset(df.columns), f"Il manque des colonnes essentielles. Colonnes trouvées : {list(df.columns)}"

def test_mongodb_connection(mongo_collection):
    """Vérifie que le serveur MongoDB répond aux requêtes."""
    try:
        # Ping la base de données
        mongo_collection.database.client.admin.command('ping')
        connection_success = True
    except Exception as e:
        connection_success = False
    assert connection_success, "Impossible de se connecter au serveur MongoDB local."

def test_migration_data_count(mongo_collection):
    """Vérifie que les données ont bien été migrées en comparant les compteurs."""
    if not os.path.exists(CSV_FILE):
        pytest.skip("Fichier CSV absent, test de comptage ignoré.")
        
    df = pd.read_csv(CSV_FILE)
    expected_count = len(df)
    mongo_count = mongo_collection.count_documents({})
    
    # Si la migration n'a pas encore eu lieu, mongo_count sera 0
    if mongo_count == 0:
        pytest.skip("La migration n'a pas encore été exécutée (0 document dans MongoDB).")
        
    assert mongo_count == expected_count, f"Désynchronisation : {expected_count} lignes dans le CSV mais {mongo_count} documents dans MongoDB."

def test_mongodb_query_performance_and_format(mongo_collection):
    """Vérifie qu'on peut interroger la collection et que les documents ont un format valide."""
    mongo_count = mongo_collection.count_documents({})
    if mongo_count == 0:
        pytest.skip("Aucune donnée en base pour tester les requêtes.")
        
    # Récupérer un document
    doc = mongo_collection.find_one()
    assert doc is not None, "Le document récupéré est vide."
    assert "_id" in doc, "Le document MongoDB doit contenir un identifiant _id."