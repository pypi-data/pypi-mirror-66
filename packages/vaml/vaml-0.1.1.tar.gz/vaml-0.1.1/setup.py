# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vaml']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'click>=7.1.1,<8.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['vaml = vaml.vaml:main']}

setup_kwargs = {
    'name': 'vaml',
    'version': '0.1.1',
    'description': 'Azure DevOps Variable Groups as YAML files',
    'long_description': "# vaml: Azure DevOps Variable Groups as YAML files\n\nvaml helps you get Azure DevOps variable groups as simple YAML files,\nmaking it easier than the current UI to modify a large amount of variable groups,\nwhile also allowing to put them back into the AZDO Library.\n\n## Introduction\n\n`vaml` is a tool to get and put Azure DevOps variable groups as files in YAML format.\n\n## Why?\n\nWhen you have multiple variable group to modify, the Azure DevOps interface can be a nuescence,\ngoing back and forth between variable groups while searching means you have to search again, and again,\nand again, this is very time consuming.\n\nSo I wanted a tool to obtain one, many or all variable groups in a project in one sweep, modify them locally,\nand them put them back.\n\n## Usage\n\nVAML requires 3 things:\n- Organization\n- Project\n- Personal Access Token (Please create this in Azure DevOps)\n\nThey can be set as environment variables:\n- VAML_ORGANIZATION\n- VAML_PROJECT\n- VAML_PAT\n\nExample:\n```\nexport VAML_ORGANIZATION=ExampleOrg\nexport VAML_PROJECT=ExampleProject\nexport VAML_PAT=accesstokengoeshere\nvaml get 'project-testing*'\n```\n\nAs a config file in (~/.vaml.cfg)\n```\norganization: ExampleOrg\nproject: ExampleProject\npat: accesstokengoeshere\n```\n\nExample: `vaml get 'project-testing*'`\n\nOr as arguments:\n`./vaml --organization ExampleOrg --project ExampleProject -pat accesstokengoeshere get 'testing-project*'` to get the arguments per command.\n\nCurrently supported commands:\n- get\n- put\n\n## Caveats\n\nCurrently only GET and PUT operations are allowed, so there's the following Todo\n\n## Todo\n\n- Create and delete operations\n- Ability to identify mixed operations, update and create for one-off operations\n",
    'author': 'Miguel A. Alvarado V.',
    'author_email': 'alvaradoma@gmail.com',
    'maintainer': 'Miguel A. Alvarado V.',
    'maintainer_email': 'alvaradoma@gmail.com',
    'url': 'https://github.com/exodus/vaml/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
