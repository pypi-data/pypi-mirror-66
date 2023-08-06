# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cvtrafficregenerator']

package_data = \
{'': ['*']}

install_requires = \
['cvapianalyser>=1.2,<2.0', 'openapispecdiff']

entry_points = \
{'console_scripts': ['cvtrafficregenerator = '
                     'cvtrafficregenerator.CVTrafficRegenerator:main']}

setup_kwargs = {
    'name': 'cvtrafficregenerator',
    'version': '1.0.2',
    'description': 'To regenerate events traffic in CloudVector API Shark when there is change in API spec',
    'long_description': "# cvtrafficregenerator\n\nCV-TrafficRegenerator is a Python library for regenerating the API events captured in CloudVector's APIShark tool with \nthe new additions when there are changes in the APISpec \n\nVisit https://www.cloudvector.com/api-shark-free-observability-security-monitoring-tool/#apishark\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.\n\n```bash\npip install cvtrafficregenerator\n```\n\n## Usage\n\n```python cvtrafficregenerator \n\n****************************************************************************************************\nCloudVector CommunityEdition - Coverage analysis plugin\n****************************************************************************************************\n\nEnter CommunityEdition(CE) host in format <host>:<port> : x.x.x.x:y\nEnter your CommunityEdition(CE) username : sandeep\nCommunityEdition(CE) password:\nEnter absolute path to Old API SPEC: ../input.json\nEnter absolute path to new API SPEC : ../input1.json \n```\n\ninstead of giving inputs every single time you can also alternatively create a file called my_cesetup.yaml in the path from where you are running the tool\n\n```yaml \nce_host:\nce_username:\nce_recording:\ninput_apispec:\n```\nyou can have multiple such my_cesetup.yaml for different CE setup or different recordings and run them from specific paths for its corresponding reports\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)",
    'author': 'Bala Kumaran',
    'author_email': 'balak@cloudvector.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
