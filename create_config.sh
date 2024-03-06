#!/bin/bash
mkdir -p ~/.config/transfer_file
if [ ! -f "routes.yaml" ]; then
    echo "arquivo routes.yaml não encontrado"
    exit 1
fi
echo "criando arquivo de configuração"


# se a flag -f for usada, o arquivo será sobrescrito
if [[ -f ~/.config/transfer_file/routes.yaml ]] && [[ ! "$1" == "-f" ]]; then
    echo "arquivo já existe, use a flag -f para sobrescrever"
    exit 1
fi
cp routes.yaml ~/.config/transfer_file
echo "arquivo de configuração criado com sucesso"