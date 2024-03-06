mkdir -p ~/.config/transfer_file
if [ ! -f "routes.yaml" ]; then
    echo "arquivo routes.yaml não encontrado"
    exit 1
fi
cp routes.yaml ~/.config/transfer_file/routes.yaml