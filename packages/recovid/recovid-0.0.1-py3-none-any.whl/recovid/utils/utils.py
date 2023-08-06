import requests
from requests.exceptions import HTTPError, ConnectionError


def get(url: str = '', timeout: int = 10):
  try:
    r = requests.get(url, timeout=timeout)
    return r.text
  except ConnectionError:
    print(f'Cannot connect to {url}')
    print(f'Remember to turn Internet ON in the Kaggle notebook settings')
  except HTTPError:
    print('Got http error', r.status, r.text)


def doi_url(id: str = ''):
  r"""
  Convert the doi to a url
  """
  return f'http://{id}' if id.startswith('doi.org') else f'http://doi.org/{id}'
