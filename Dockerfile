# Utiliser une image Python officielle
FROM python:3.13
FROM nginx:latest
COPY nginx.conf /etc/nginx/nginx.conf

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt


# Exposer le port 8000 pour Gunicorn
EXPOSE 8000

FROM nginx:latest
COPY nginx.conf /etc/nginx/nginx.conf
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the application (update as needed)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]


# Lancer l'application avec Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]


