import requests


def search_avatar(user):
    """
    Busca o avatar de um usuário no Github
    :param user: str with username on github
    :return: str with avatar link
    """

    url = f'https://api.github.com/users/{user}'
    resp = requests.get(url)
    return resp.json()['avatar_url']


if __name__ == '__main__':
    print(search_avatar('lidymonteiro'))
