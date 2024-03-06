#!/bin/bash

#check if routes.yaml exists
if [ ! -f "routes.yaml" ]; then
    echo "arquivo routes.yaml não encontrado"
    exit 1
fi

poetry install
poetry build -f wheel
pipx install dist/*.whl --force
./create_config.sh

echo "Instalação concluída com sucesso!"