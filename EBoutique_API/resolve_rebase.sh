#!/bin/bash

# Vérifie que tu es en plein rebase
if [ ! -d ".git/rebase-apply" ] && [ ! -d ".git/rebase-merge" ]; then
  echo "Tu n'es pas en train de faire un rebase."
  exit 1
fi

# Liste tous les fichiers conflictuels
files=$(git diff --name-only --diff-filter=U)

if [ -z "$files" ]; then
  echo "Aucun fichier en conflit."
  git rebase --continue
  exit 0
fi

echo "Résolution automatique des conflits en faveur de la branche distante (--theirs)..."

for file in $files; do
  echo "Traitement de $file"
  git checkout --theirs -- "$file"
  git add "$file"
done

echo "Tous les fichiers conflictuels ont été pris côté distant."
echo "Continuation du rebase..."

git rebase --continue
