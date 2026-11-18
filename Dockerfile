# Utiliser une image officielle Python légère
FROM python:3.11-slim

# Définir le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# Copier d'abord le fichier des dépendances pour optimiser le cache Docker
COPY requirements.txt .

# Installer les dépendances sans stocker de caches superflus
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le reste du code source du projet dans le conteneur
COPY . .

# Commande exécutée par défaut au lancement du conteneur
CMD ["python", "migrate.py"]