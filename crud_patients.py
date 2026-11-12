from pymongo import MongoClient

# 1. Connexion au serveur MongoDB local
client = MongoClient("mongodb://localhost:27017/")

# 2. Création (ou sélection) de la base de données et de la collection
db = client["medical_db"]
collection = db["patients"]

print(f"Base de données connectée : {db.name}")
print(f"Collection active : {collection.name}\n")

# Nettoyage préalable pour l'exemple (optionnel)
collection.delete_many({})

# ==========================================
# C - CREATE (Création / Insertion de documents)
# ==========================================
print("--- 1. INSERTION (CREATE) ---")

# Insertion d'un document unique (Patient 1)
patient_1 = {
    "patient_id": "PAT_001",
    "age": 45,
    "genre": "M",
    "diagnostic": "Hypertension",
    "statut_suivi": "Actif"
}
result_one = collection.insert_one(patient_1)
print(f"Patient unique inséré avec l'ID BSON : {result_one.inserted_id}")

# Insertion multiple (Patients 2 et 3 issus du dataset)
patients_batch = [
    {
        "patient_id": "PAT_002",
        "age": 32,
        "genre": "F",
        "diagnostic": "Diabète Type 2",
        "statut_suivi": "En attente"
    },
    {
        "patient_id": "PAT_003",
        "age": 58,
        "genre": "M",
        "diagnostic": "Saine",
        "statut_suivi": "Clôturé"
    }
]
result_many = collection.insert_many(patients_batch)
print(f"Nombre de documents insérés en bloc : {len(result_many.inserted_ids)}\n")


# ==========================================
# R - READ (Lecture / Requêtage)
# ==========================================
print("--- 2. LECTURE (READ) ---")

# Recherche d'un seul document spécifique
query_one = collection.find_one({"patient_id": "PAT_001"})
print("Patient trouvé (PAT_001) :", query_one)

# Recherche de plusieurs documents selon un filtre (ex: âge supérieur à 40 ans)
print("\nPatients de plus de 40 ans :")
query_many = collection.find({"age": {"$gt": 40}})
for doc in query_many:
    print(f"- {doc['patient_id']} : {doc['diagnostic']} ({doc['age']} ans)")


# ==========================================
# U - UPDATE (Mise à jour)
# ==========================================
print("\n--- 3. MISE À JOUR (UPDATE) ---")

# Modification du statut de suivi pour le patient PAT_002
update_result = collection.update_one(
    {"patient_id": "PAT_002"},
    {"$set": {"statut_suivi": "Actif", "remarque": "Traitement initié"}}
)
print(f"Documents modifiés : {update_result.modified_count}")

# Vérification de la modification
updated_doc = collection.find_one({"patient_id": "PAT_002"})
print("Document mis à jour :", updated_doc)


# ==========================================
# D - DELETE (Suppression)
# ==========================================
print("\n--- 4. SUPPRESSION (DELETE) ---")

# Suppression d'un document spécifique (ex: dossier clôturé PAT_003)
delete_result = collection.delete_one({"patient_id": "PAT_003"})
print(f"Documents supprimés : {delete_result.deleted_count}")

# Vérification du nombre total de documents restants dans la collection
total_docs = collection.count_documents({})
print(f"Nombre total de patients dans la collection : {total_docs}")

# Fermeture de la connexion
client.close()