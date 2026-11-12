import os
import pandas as pd
from pymongo import MongoClient, IndexModel, ASCENDING
from datetime import datetime

# Configuration
CSV_FILE = "healthcare_dataset.csv"
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "medical_db"
COLLECTION_NAME = "patients"
BATCH_SIZE = 10000  # Nombre de documents insérés par lot pour optimiser la mémoire

def clean_and_prepare_data(df):
    """Nettoie et convertit les types des données du dataset médical."""
    print("🧹 Nettoyage et typage des données en cours...")
    
    # 1. Nettoyage des noms de colonnes (suppression des espaces superflus si existants)
    df.columns = df.columns.str.strip()
    
    # 2. Conversion des types numériques (ex: Age, Billing Amount)
    if 'Age' in df.columns:
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    if 'Billing Amount' in df.columns:
        df['Billing Amount'] = pd.to_numeric(df['Billing Amount'], errors='coerce')
        
    # 3. Conversion des dates (Date of Admission, Discharge Date)
    if 'Date of Admission' in df.columns:
        df['Date of Admission'] = pd.to_datetime(df['Date of Admission'], errors='coerce')
    if 'Discharge Date' in df.columns:
        df['Discharge Date'] = pd.to_datetime(df['Discharge Date'], errors='coerce')
        
    # Remplacement des valeurs NaN par None pour compatibilité BSON/MongoDB propre
    df = df.where(pd.notnull(df), None)
    
    return df

def run_migration():
    print("=" * 60)
    print("🚀 DÉBUT DE LA MIGRATION VERS MONGODB")
    print("=" * 60)
    
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(f"Le fichier source '{CSV_FILE}' est introuvable dans le dossier.")
    
    # 1. Chargement du CSV avec Pandas
    print(f"📖 Chargement du fichier CSV : {CSV_FILE}...")
    df = pd.read_csv(CSV_FILE)
    total_rows = len(df)
    print(f"-> {total_rows} lignes chargées depuis le CSV.")
    
    # 2. Nettoyage
    df = clean_and_prepare_data(df)
    
    # 3. Connexion MongoDB
    print(f"🔌 Connexion à MongoDB ({MONGO_URI})...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    # 4. Création des index pertinents pour la recherche médicale
    print("index Création des index (Medical Condition, Age)...")
    collection.create_indexes([
        IndexModel([("Medical Condition", ASCENDING)]),
        IndexModel([("Age", ASCENDING)])
    ])
    
    # 5. Nettoyage préalable de la collection (optionnel : évite les doublons si relancé)
    print(f"🗑️ Nettoyage de la collection '{COLLECTION_NAME}' avant insertion...")
    collection.delete_many({})
    
    # 6. Insertion par lots (Bulk Insert par chunks)
    print(f"📥 Insertion des données par lots de {BATCH_SIZE} documents...")
    data_dicts = df.to_dict(orient="records")
    
    inserted_count = 0
    for i in range(0, len(data_dicts), BATCH_SIZE):
        batch = data_dicts[i:i + BATCH_SIZE]
        if batch:
            result = collection.insert_many(batch)
            inserted_count += len(result.inserted_ids)
            print(f"   -> {inserted_count} / {total_rows} documents insérés...")
            
    print("=" * 60)
    print(f"✅ MIGRATION TERMINÉE AVEC SUCCÈS !")
    print(f"📊 Total de documents dans MongoDB : {collection.count_documents({})}")
    print("=" * 60)
    
    client.close()

if __name__ == "__main__":
    run_migration()