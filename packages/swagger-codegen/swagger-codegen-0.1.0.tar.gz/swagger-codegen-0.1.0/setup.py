# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['swagger_codegen',
 'swagger_codegen.api',
 'swagger_codegen.api.adapter',
 'swagger_codegen.cli',
 'swagger_codegen.parsing',
 'swagger_codegen.render',
 'swagger_codegen.render.post_processors']

package_data = \
{'': ['*'], 'swagger_codegen': ['templates/package_renderer/*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'inflection>=0.4.0,<0.5.0',
 'jinja2>=2.11.1,<3.0.0',
 'multidict>=4.7.5,<5.0.0',
 'pydantic>=1.4,<2.0',
 'rich>=0.8.11,<0.9.0',
 'toml>=0.10.0,<0.11.0',
 'typer>=0.1.1,<0.2.0']

extras_require = \
{'all': ['aiohttp', 'requests', 'black>=19.10b0,<20.0'],
 'async': ['aiohttp'],
 'black': ['black>=19.10b0,<20.0'],
 'sync': ['requests']}

entry_points = \
{'console_scripts': ['swagger_codegen = swagger_codegen.cli.main:app']}

setup_kwargs = {
    'name': 'swagger-codegen',
    'version': '0.1.0',
    'description': 'Generate API clients by parsing Swagger definitions',
    'long_description': None,
    'author': 'asyncee',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
