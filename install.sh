#!/bin/bash

if [ $# -eq 0 ]; then
    echo "usage: $0 <dest_dir>"
    exit 1 
fi

#check if routes.yaml exists
if [ ! -f "routes.yaml" ]; then
    echo "arquivo routes.yaml não encontrado"
    exit 1
fi

dest_dir="$1"

export PYINSTALLER_NO_PROGRESS_BAR=1

poetry install

poetry run pyinstaller --onefile transfer_file/ssh_to_server.py --clean
poetry run pyinstaller --onefile transfer_file/transfer.py --clean

rm -f *.spec

dest_dir="$HOME/scripts"

mkdir -p "$dest_dir"

cp -v dist/ssh_to_server "$dest_dir"
cp -v dist/transfer "$dest_dir"
cp -v routes.yaml "$dest_dir"

echo "Instalação concluída com sucesso!"