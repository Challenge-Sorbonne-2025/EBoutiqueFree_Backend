# EBoutiqueFree_Backend
## Trouver la boutique free la plus proche 

Ce projet est une API REST développée avec Django Rest Framework (DRF) qui permet de gérer les boutiques Free et leurs produits. Il utilise PostgreSQL comme base de données.

## Prérequis

- Python 3.10 ou supérieur
- PostgreSQL
- pip (gestionnaire de paquets Python)

## Installation et Configuration

1. Cloner le projet :
```bash
git clone [git@github.com:Challenge-Sorbonne-2025/EBoutiqueFree_Backend.git]
cd EBoutiqueFree_Backend
```

2. Créer un environnement virtuel (recommandé) :
```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate  # Sur Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer la base de données PostgreSQL :
   - Créer une base de données PostgreSQL
   - Mettre à jour les paramètres de connexion dans `EBoutique_API/settings.py`

5. Effectuer les migrations :
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Créer un superutilisateur (admin) :
```bash
python manage.py createsuperuser
```

7. Lancer le serveur de développement :
```bash
python manage.py runserver
```

## Structure du Projet

- `eboutique_config/` : Configuration principale du projet Django
  - `settings.py` : Configuration du projet
  - `urls.py` : Configuration des URLs principales
- `boutique/` : Application principale pour  tous ce qui est relations avec les boutiques
  - `models.py` : Définition des modèles de données
  - `views.py` : Logique de l'application
  - `urls.py` : Configuration des URLs de l'application
  - `serializers.py` : Sérialisation des données pour l'API

- `free_app/`: Configuration de l'application free_app (tous ce qui est liées aux utilisateurs)
  - `models.py` : Définition des modèles de données pour les utiliisateurs
  - `views.py` : Vue logique de l'application
  - `urls.py` : Configuration des URLs de l'application
  - `serializers.py` : Sérialisation des données pour l'API

## Modèles Principaux

- `Boutique` : Gère les informations des boutiques Free
- `Produit` : Gère les produits disponibles
- `User` : Gestion des utilisateurs avec différents rôles (responsable, gestionnaire)

## Bonnes Pratiques de Développement

### Gestion des Branches Git

1. La branche `main` est protégée, ne pas faire de push direct dessus
2. Utiliser la branche `dev` comme base pour le développement
3. Créer une branche personnelle à partir de `dev` (ex: `dev-aby`)
4. Workflow recommandé :
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b dev-votre-nom
   # Faire vos modifications
   git add .
   git commit -m "Description des modifications"
   git push origin dev-votre-nom
   ```

### Vérifications Avant Commit

1. Vérifier l'état du dépôt :
```bash
git status
git status uno
```

2. Vérifier les modifications :
```bash
git diff
```

3. Vérifier les conflits potentiels :
```bash
git fetch origin
git merge origin/dev
```

## Points Importants à Noter

- Les numéros de téléphone et adresses email doivent être uniques
- Utiliser des migrations pour toute modification de la base de données
- Documenter les nouvelles fonctionnalités
- Tester les endpoints API avant de les mettre en production
- Pour les tests avec la connexion avec swagger, faite bien attention et separer le prefixe `Bearer` et le `token` avec un `space ( )` 

## Ressources Utiles

- [Documentation Django](https://docs.djangoproject.com/)
- [Documentation Django REST Framework](https://www.django-rest-framework.org/)
- [Documentation PostgreSQL](https://www.postgresql.org/docs/)

## Support

Pour toute question ou problème, veuillez créer une issue dans le dépôt GitHub.

```bash
pip install -r requirements.txt
```

## Fichier .env.example

Le fichier `.env.example` est un modèle qui contient les variables d'environnement nécessaires au fonctionnement de l'application. Pour l'utiliser :

1. Copiez le fichier `.env.example` et renommez la copie en `.env`
2. Remplissez les valeurs des variables dans le fichier `.env` avec vos propres paramètres :

## Update Database postgis
1. install postgis extension
 ```bash
 sudo -u postgres psql 
 # ensuite ta la commande suivantes
 CREATE EXTENSION postgis;
 # verifie l'installation avec :
 SELECT PostGIS_Version();
 ```
 