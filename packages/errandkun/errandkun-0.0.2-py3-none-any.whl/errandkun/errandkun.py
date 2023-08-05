import sys
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from .external_resources.github import GithubArtefactSource
import os

class ErrandKunPlugin(BasePlugin):

  config_scheme = (
    ('extract_path', config_options.Type(str, required=True)),
    ('external_resources', config_options.Type(list, default=[])),
    ('ver', config_options.Type(int, default=0))
  )

  def on_pre_build(self, config):
    
    extract_path = self.config['extract_path']

    for external_resource in self.config['external_resources']:
      if external_resource['type'] is None:
        raise Exception(f'type needs to be defined in external_resources')
      if external_resource['type'].lower() == 'github':
        github = GithubArtefactSource(
                    extract_path=extract_path,
                    github_owner=external_resource['owner'],
                    github_repo=external_resource['repo'],
                    workflow_name=external_resource['workflow_name'],
                    token=os.getenv('ERRANDKUN_GITHUB_TOKEN', default=None))
        github.download_all()
    print('hello there', )
    pass