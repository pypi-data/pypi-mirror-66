# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vcr_stub_server', 'vcr_stub_server.cassettes']

package_data = \
{'': ['*']}

install_requires = \
['vcrpy>=4.0.2,<5.0.0']

entry_points = \
{'console_scripts': ['poetry = vcr_stub_server.__main__:main']}

setup_kwargs = {
    'name': 'vcr-stub-server',
    'version': '0.1.1',
    'description': 'Standalone stub server for replaying VCR cassettes',
    'long_description': '# vcr-stub-server\n\n## Usage\n\n```\nvcr-stub-server path/to/vcr_cassette.yml\n```',
    'author': 'Simon Nizov',
    'author_email': 'simon.nizov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
