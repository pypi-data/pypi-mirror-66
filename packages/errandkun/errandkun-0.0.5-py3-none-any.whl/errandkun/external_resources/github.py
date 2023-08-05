from .base import BaseExternalSource, MissingParameter, UnexpectedListLength
import requests
import json
from zipfile import ZipFile
import os

GITHUB_API_ENDPOINT = 'https://api.github.com'

class GithubArtefactSource(BaseExternalSource):
  """
  external resource, retrieving github artefacts
  """

  def __init__(self, github_owner, github_repo, token, workflow_name, extract_path):
    super().__init__(extract_path=extract_path)
    self.github_owner = github_owner
    self.github_repo = github_repo
    self.token = token
    self.workflow_name = workflow_name

  def validate(self):
    if self.github_owner is None:
      raise MissingParameter('github_owner is required, but missing')

    if self.github_repo is None:
      raise MissingParameter('github_repo is required, but missing')

  def download_all(self):
    if self.workflow_name is None:
      raise MissingParameter('workflow_name is required for download_all, but missing')
    workflows = self.get_all_workflows()
    filtered_workflows = [workflow for workflow in workflows if workflow['name'] == self.workflow_name]
    if len(filtered_workflows) != 1:
      workflow_names = ', '.join([workflow['name'] for workflow in workflows])
      raise UnexpectedListLength(f'workflow names: {workflow_names} filtered by supplied workflow_name: {self.workflow_name} results in length {len(filtered_workflows)}')
    runs = self.get_workflow_runs(workflow_id=filtered_workflows[0]['id'])
    if len(runs) < 1:
      raise UnexpectedListLength(f'querying runs result in length < 1: {len(runs)}')

    # get all runs that are a/ completed and b/ successful
    filtered_runs = [ run for run in runs if run['status'] == 'completed' and run['conclusion'] == 'success' ]
    if len(filtered_runs) < 1:
      raise UnexpectedListLength('no runs are both completed and successful')
    
    for run in filtered_runs:
      artifacts = self.get_artifacts(run_id=run['id'])
      if len(artifacts) > 0:

        zip_archives=[]

        for artifact in artifacts:

          download_url=artifact['archive_download_url']
          artifact_id=artifact['id']
          filename=f'artiface_{artifact_id}.zip'
          headers=self.get_github_call_header()

          path_to_zip=self.download(url=download_url, filename=filename, headers=headers)
          zip_archives.append(path_to_zip)
          
        for zip_archive in zip_archives:
          # unzips all files
          with ZipFile(zip_archive, 'r') as zipObj:
            zipObj.extractall(self.extract_path)

          # remove zip archive
          os.remove(zip_archive)

        # only extract the latest run with artefacts
        break

  def get_github_call_header(self):
    return {'authorization': f'token {self.token}'} if self.token is not None else {}

  def call_github_restapi(self, url):
    self.validate()
  
    r = requests.get(url, headers=self.get_github_call_header())
    r.raise_for_status()
    return r.json()

  def get_all_workflows(self):
    response_json = self.call_github_restapi(f'{GITHUB_API_ENDPOINT}/repos/{self.github_owner}/{self.github_repo}/actions/workflows')
    return response_json['workflows']

  def get_workflow_runs(self, workflow_id=None):
    if workflow_id is None:
      raise MissingParameter('workflow_id is required for get_workflow_runs')
    response_json = self.call_github_restapi(f'{GITHUB_API_ENDPOINT}/repos/{self.github_owner}/{self.github_repo}/actions/workflows/{workflow_id}/runs')
    return response_json['workflow_runs']

  def get_artifacts(self, run_id=None):
    url = f'{GITHUB_API_ENDPOINT}/repos/{self.github_owner}/{self.github_repo}/actions/runs/{run_id}/artifacts' if run_id is not None else f'{GITHUB_API_ENDPOINT}/repos/{self.github_owner}/{self.github_repo}/actions/artifacts'
    response_json = self.call_github_restapi(url)
    return response_json['artifacts']