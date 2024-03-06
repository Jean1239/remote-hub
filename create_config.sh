#!/bin/bash

mkdir -p ~/.config/transfer_file

echo "criando arquivo de configuração"


# se a flag -f for usada, o arquivo será sobrescrito
if [[ -f ~/.config/transfer_file/routes.yaml ]]; then
    echo "arquivo já existe"
    exit 1
fi

cp routes_example.yaml ~/.config/transfer_file/routes.yaml
echo "arquivo de configuração criado com sucesso"
echo "adicione rotas em ~/.config/transfer_file/routes.yaml"