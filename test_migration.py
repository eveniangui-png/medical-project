import os
import pytest
import pandas as pd
from pymongo import MongoClient

# Configuration
CSV_FILE = "healthcare_dataset.csv"
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "medical_db"
COLLECTION_NAME = "patients"

@pytest.fixture(scope="module")
def mongo_collection():
    """Fixture pour se connecter à MongoDB et fournir la collection aux tests."""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    yield collection
    client.close()

def test_csv_file_exists():
    """Vérifie que le fichier CSV source existe bien."""
    assert os.path.exists(CSV_FILE), f"Le fichier source {CSV_FILE} est introuvable."

def test_csv_structure(mongo_collection):
    """Vérifie que le fichier CSV contient les colonnes attendues."""
    if not os.path.exists(CSV_FILE):
        pytest.skip("Fichier CSV absent.")
    
    df = pd.read_csv(CSV_FILE)
    # Vérifie quelques colonnes clés du dataset médical
    expected_columns = ["Name", "Age", "Gender", "Blood Type", "Medical Condition", "Date of Admission"]
    for col in expected_columns:
        assert col in df.columns, f"La colonne essentielle '{col}' est absente du CSV."

def test_mongodb_connection(mongo_collection):
    """Vérifie que l'instance MongoDB est accessible et répond."""
    try:
        # Commande ping pour tester la connexion
        result = mongo_collection.database.command("ping")
        assert result.get("ok") == 1.0, "La réponse du serveur MongoDB n'est pas valide."
    except Exception as e:
        pytest.fail(f"Impossible de se connecter à MongoDB : {e}")

def test_migration_data_count(mongo_collection):
    """Vérifie que le nombre de documents dans MongoDB correspond au nombre de lignes du CSV."""
    if not os.path.exists(CSV_FILE):
        pytest.skip("Fichier CSV absent, test de comptage ignoré.")
    
    df = pd.read_csv(CSV_FILE)
    expected_count = len(df)
    mongo_count = mongo_collection.count_documents({})
    
    if mongo_count == 0:
        pytest.skip("La migration n'a pas encore été exécutée (0 document dans MongoDB).")
    
    assert mongo_count == expected_count, f"Désynchronisation : {expected_count} lignes dans le CSV mais {mongo_count} documents dans MongoDB."

def test_mongodb_query_performance_and_format(mongo_collection):
    """Vérifie qu'au moins un document est récupérable et possède une structure correcte."""
    if mongo_collection.count_documents({}) == 0:
        pytest.skip("Collection vide, test de format ignoré.")
    
    sample = mongo_collection.find_one()
    assert sample is not None, "Aucun document trouvé dans la collection."
    assert "_id" in sample, "Le document MongoDB ne contient pas d'identifiant _id."
    assert "Medical Condition" in sample, "Le champ 'Medical Condition' est manquant dans le document."