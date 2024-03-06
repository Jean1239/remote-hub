#!/bin/bash

poetry install
poetry build -f wheel
pipx install dist/*.whl --force

./create_config.sh

echo "Instalação concluída com sucesso!"