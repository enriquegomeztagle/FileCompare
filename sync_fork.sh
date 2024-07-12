#!/bin/bash

# Definir colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Verificar si el remoto upstream está configurado
UPSTREAM_URL=$(git remote get-url upstream 2>/dev/null)
if [ "$UPSTREAM_URL" != "git@github.com:LoloREIN/FileCompare.git" ]; then
    echo -e "${YELLOW}Configuring upstream remote...${NC}"
    git remote add upstream git@github.com:LoloREIN/FileCompare.git 2>/dev/null || git remote set-url upstream git@github.com:LoloREIN/FileCompare.git
else
    echo -e "${GREEN}Upstream remote is already configured.${NC}"
fi

# Verificar si el remoto origin está configurado
ORIGIN_URL=$(git remote get-url origin 2>/dev/null)
if [ "$ORIGIN_URL" != "git@github.com:enriquegomeztagle/FileCompare.git" ]; then
    echo -e "${YELLOW}Configuring origin remote...${NC}"
    git remote set-url origin git@github.com:enriquegomeztagle/FileCompare.git
else
    echo -e "${GREEN}Origin remote is already configured.${NC}"
fi

# Obtener los cambios del repositorio original
echo -e "${BLUE}Fetching updates from upstream...${NC}"
git fetch upstream

# Cambiar a tu rama principal
echo -e "${BLUE}Checking out main branch...${NC}"
git checkout main

# Fusionar los cambios de upstream/main en tu rama principal
echo -e "${BLUE}Merging changes from upstream/main into main branch...${NC}"
git merge upstream/main

# Subir los cambios a tu repositorio fork en GitHub
echo -e "${BLUE}Pushing changes to origin...${NC}"
git push origin main

echo -e "${GREEN}Sync completed successfully!${NC}"
