import requests


def buscar_avatar(usuario):
    """
    Busca avatar de um usuario no github

    :param usuario: str com o nome do usuario
    :return: str com o link do avatar
    """
    url = f'https://api.github.com/users/jona04'
    resp = requests.get(url)
    return resp.json()['avatar_url']


if __name__ == '__main__':
    print(buscar_avatar('jona04'))
