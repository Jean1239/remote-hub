#!/bin/bash

#check if routes.yaml exists
if [ ! -f "transfer_file/data_files/routes.yaml" ]; then
    echo "arquivo routes.yaml não encontrado"
    exit 1
fi


export PYINSTALLER_NO_PROGRESS_BAR=1

poetry install
poetry build -f wheel
pip install dist/*.whl

echo "Instalação concluída com sucesso!"