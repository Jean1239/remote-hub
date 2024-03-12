import os
import yaml

import questionary

from . import routes, Server, ROUTES_FILE_PATH


def validateText(text: str):
    return True if len(text) > 0 else "Please enter a value"


def configRoutes():
    response = questionary.select(
        "O que você quer fazer?",
        choices=[
            "Adicionar Rota",
            "Modificar Rota",
            "Remover Rota",
            "Salvar e Sair",
            "Sair sem Salvar",
        ],
    ).ask()

    if response == "Adicionar Rota":
        addRoute()
    if response == "Salvar e Sair":
        saveRoutes()
    if response == "Modificar Rota":
        ModifyRoute()
    if response == "Remover Rota":
        removeRoute()
    if response == "Sair sem Salvar":
        exit(0)


def saveRoutes():
    if not os.path.exists(ROUTES_FILE_PATH):
        os.makedirs(os.path.dirname(ROUTES_FILE_PATH), exist_ok=True)
    with open(ROUTES_FILE_PATH, "w") as file:
        routesDict = {key: value.__dict__ for key, value in routes.items()}
        yaml.dump(routesDict, file)
    exit(0)


def addRoute():
    defaultUser = os.getlogin()
    name = questionary.text(
        "Nome da rota:",
        validate=validateText,
    ).ask()
    previous = questionary.text(
        "Rota anterior (Se a rota anterior for essa máquina, coloque '.'):",
        validate=validateText,
    ).ask()
    user = questionary.text(
        "Nome do usuário:", default=defaultUser, validate=validateText
    ).ask()
    ip = questionary.text("Endereço IP ou Hostname:", validate=validateText).ask()
    port = questionary.text("Porta:", default="22", validate=validateText).ask()
    pkey_file = questionary.text(
        "Caminho para a chave privada (expansão '~' não suportada)",
        validate=validateText,
    ).ask()
    routeDict = {
        "name": name,
        "previous": previous,
        "user": user,
        "ip": ip,
        "port": int(port),
        "pkey_file": pkey_file,
    }

    server = Server(**routeDict)
    routes[name] = server


def ModifyRoute():
    response = questionary.select(
        "Escolha a rota que você quer modificar:",
        choices=[*routes.keys(), "Cancelar"],
    ).ask()

    if response == "Cancelar":
        return

    route = routes[response]

    name = questionary.text(
        "Nome da rota:",
        validate=validateText,
        default=route.name,
    ).ask()
    previous = questionary.text(
        "Rota anterior (Se a rota anterior for essa máquina, coloque '.'):",
        validate=validateText,
        default=route.previous,
    ).ask()
    user = questionary.text(
        "Nome do usuário:",
        validate=validateText,
        default=route.user,
    ).ask()
    ip = questionary.text(
        "Endereço IP ou Hostname:", validate=validateText, default=route.ip
    ).ask()
    port = questionary.text(
        "Porta:", default=str(route.port), validate=validateText
    ).ask()
    pkey_file = questionary.path(
        "Caminho para a chave privada", validate=validateText, default=route.pkey_file
    ).ask()
    routeDict = {
        "name": name,
        "previous": previous,
        "user": user,
        "ip": ip,
        "port": int(port),
        "pkey_file": pkey_file,
    }

    server = Server(**routeDict)
    routes[name] = server


def removeRoute():
    response = questionary.select(
        "Escolha a rota que você quer remover:",
        choices=[*routes.keys(), "Cancelar"],
    ).ask()

    if response == "Cancelar":
        return

    del routes[response]


def main():
    while True:
        configRoutes()
        os.system("clear")
