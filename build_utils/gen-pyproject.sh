#!/bin/bash

# Génération du pyproject.toml avec le bon numéro de version

VERSION_REPO_GIT=$(python -c "import sh_crypt;print(sh_crypt.__version__)")

sed "s/<VERSION>/$VERSION_REPO_GIT/g" build_utils/pyproject.toml.template > pyproject.toml