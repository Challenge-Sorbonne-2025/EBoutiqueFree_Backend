import os

# Chemins attendus à la racine du projet
DOSSIERS_ATTENDUS = [
    "boutique",
    "free_app",
    "EBoutique_API"
]

FICHIERS_ATTENDUS_PAR_APP = {
    "boutique": [
        "models.py",
        "views.py",
        "api_views.py",
        "urls.py",
        "apps.py",
        "__init__.py"
    ],
    "EBoutique_API": [
        "settings.py",
        "urls.py",
        "wsgi.py",
        "__init__.py"
    ]
}

def check_dossier(dossier):
    if not os.path.isdir(dossier):
        print(f"❌ Dossier manquant : {dossier}")
        return False
    print(f"✅ Dossier trouvé : {dossier}")
    return True

def check_fichiers(dossier, fichiers):
    manquants = []
    for fichier in fichiers:
        chemin = os.path.join(dossier, fichier)
        if not os.path.isfile(chemin):
            manquants.append(fichier)
    if manquants:
        print(f"❌ Dans {dossier}, fichiers manquants : {', '.join(manquants)}")
    else:
        print(f"✅ Tous les fichiers attendus sont présents dans {dossier}")

def main():
    print("🔍 Vérification de la structure du projet Django...\n")

    for dossier in DOSSIERS_ATTENDUS:
        if check_dossier(dossier):
            fichiers = FICHIERS_ATTENDUS_PAR_APP.get(dossier, [])
            check_fichiers(dossier, fichiers)
        print()

if __name__ == "__main__":
    main()
