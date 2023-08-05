#!/usr/bin/env python
import json
import requests
import yaml
import click
from sys import argv, exit
from glob import glob
from pathlib import Path

class Config(object):

    def __init__(self, organization: str = None, project: str = None, pat: str = None):
        self.organization = organization
        self.project = project
        self.pat = pat
        self.queries = {'api-version': '5.0-preview.1'}
        self.headers = {'Content-Type': 'application/json'}
        self.auth = ('Basic', self.pat)
        self.url = f'https://dev.azure.com/{self.organization}/{self.project}/_apis/distributedtask/variablegroups/'

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    auto_envvar_prefix='VAML'
)

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--organization', '-org', help='Organization to use')
@click.option('--project', '-proj', help='Project to use in the organization')
@click.option('--pat', '-pat', help='Personal Access Token')
@click.pass_context
def main(config, organization: str, project: str, pat: str):
    try:
        with open(Path('~/.vaml.cfg').expanduser()) as file:
            data = yaml.safe_load(file)
        if isinstance(data, dict):
            if 'organization' in data:
                org = data['organization']
            if 'project' in data:
                proj = data['project']
            if 'pat' in data:
                token = data['pat']
    except:
        pass
    if organization:
        org = organization
    if project:
        proj = project
    if pat:
        token = pat

    try:
        config.obj = Config(org, proj, token)
    except:
        exit("Missing Parameter from config file or options. Check Org, Project or PAT")
    

def config(organization: str, project: str, pat: str):
    '''Store configuration on file'''
    

def get_var(config: Config, var_group: str):
    '''Fetch the variable group JSON, does not write to file'''
    
    config.obj.queries.update({'groupName': var_group})
    resp = requests.get(config.obj.url, auth=config.obj.auth, params=config.obj.queries)
    if resp.status_code != 200:
        exit('Issues getting the variable groups. Check your settings (Organization, Project or PAT)')
    data = resp.json()
    if data['value']:
        return data['value']
    else:
        print("No variable group found")
        exit(1)

@main.command()
@click.argument('var_group')
@click.pass_context
def get(config, var_group: str):
    '''Get the variable group(s)
        You can use a glob pattern to get multiple'''
    vars = get_var(config, var_group)
    for var in vars:
        name = var['name']
        print(f"Fetching {name}")
        with open(f"{name}.yaml", "w") as f:
            yaml.dump(var, f)

@main.command()
@click.argument('var_group')
@click.pass_context
def put(config, var_group: str):
    '''Put variable group(s)
        You can use a glob pattern to put multiple'''
    files = glob(var_group)
    if files:
        for file in files:
            with open(file) as file:
                data = yaml.safe_load(file)
            payload =   {'type': 'Vsts',
                        'name': data['name'],
                        'description': '',
                        'variables': data['variables']}
            config.obj.queries.update({'groupId': data['id']})
            print(f"Posting {file.name}")
            requests.put(config.obj.url, data=json.dumps(payload), auth=config.obj.auth, headers=config.obj.headers, params=config.obj.queries)
    else:
        print("No file match")
        exit(1)

if __name__ == '__main__':
    main()
