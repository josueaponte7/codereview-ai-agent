import requests
from core.config import GITHUB_TOKEN


def get_user(user_id):
    # Lógica de negocio mezclada con acceso a datos
    url = f"https://api.github.com/users/{user_id}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Validación mezclada con transformación
    if data:
        name = data.get("name")
        email = data.get("email")
        repos = data.get("public_repos")
        print(f"User: {name}, {email}, {repos}")
        return data
    else:
        return None


def save_user(u):
    # Nombre de parámetro sin significado
    print(f"Saving {u}")
    # Sin persistencia real, sin manejo de errores
    pass


def doStuff(x, y, z):
    # Nombre sin significado, múltiples responsabilidades
    result = get_user(x)
    save_user(result)
    print(y, z)
    return result