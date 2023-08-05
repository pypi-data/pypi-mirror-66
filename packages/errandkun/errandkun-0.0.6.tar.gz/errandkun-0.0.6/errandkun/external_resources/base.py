import requests
from os import path, makedirs
import uuid

class BaseExternalSource():
  """
  base class for external resources
  """
  def __init__(self, extract_path=None):
    print('path', extract_path)
    self.extract_path = extract_path
    pass

  def download(self, url, headers=None, filename=None):
    if url is None:
      raise MissingParameter('url is required for download function')
    makedirs(self.extract_path, exist_ok=True)
    r = requests.get(url, headers=headers)
    _filename = filename if filename is not None else uuid.uuid4()
    with open(path.join(self.extract_path, _filename), 'wb') as f:
      f.write(r.content)
    return path.join(self.extract_path, _filename)

  def download_all(self):
    """
    Should be overwritten by subclasses
    """
    pass

class MissingParameter(Exception):
  """
  Missing parameter Exception
  """
  pass

class UnexpectedListLength(Exception):
  """
  Unexpected length
  """
  pass