# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyotr',
 'pyotr.validation',
 'pyotr.validation.requests',
 'pyotr.validation.responses']

package_data = \
{'': ['*']}

install_requires = \
['http3>=0.6.3,<0.7.0',
 'httpx>=0.7.2,<0.8.0',
 'openapi-core>=0.13.1,<0.14.0',
 'pyyaml>=5.1,<6.0',
 'starlette>=0.13,<0.14',
 'stringcase>=1.2,<2.0',
 'typing-extensions>=3.7,<4.0',
 'werkzeug>=1.0.0,<2.0.0']

extras_require = \
{':extra == "uvicorn"': ['uvicorn>=0.9.0,<0.10.0']}

setup_kwargs = {
    'name': 'pyotr',
    'version': '0.4.7',
    'description': 'Python OpenAPI-to-REST (and back) framework ',
    'long_description': 'Pyotr\n=====\n\n[![Documentation Status](https://readthedocs.org/projects/pyotr/badge/?version=latest)](https://pyotr.readthedocs.io/en/latest/)\n[![CI builds](https://b11c.semaphoreci.com/badges/pyotr.svg?style=shields)](https://b11c.semaphoreci.com/projects/pyotr)\n\n**Pyotr** is a Python library for serving and consuming REST APIs based on \n[OpenAPI](https://swagger.io/resources/open-api/) specifications. Its name is acronym of "Python OpenAPI to REST".\n\nThe project consists of two separate libraries that can be used independently:\n\n* `pyotr.server` is a [Starlette](https://www.starlette.io)-based framework for serving OpenAPI-based services. \n  It is functionally very similar to [connexion](https://connexion.readthedocs.io), except that it aims to be fully \n  [ASGI](https://asgi.readthedocs.io)-compliant. \n* `pyotr.client` is a HTTP client for consuming OpenAPI-based services.\n\n**WARNING:** This is still very much work in progress and not quite ready for production usage. Until version 1.0 is \nreleased, any version can be expected to break backward compatibility.\n\n\nQuick Start\n-----------\n\n### Server\n\n    from pyotr.server import Application\n    from some.path import endpoints\n    \n    app = Application.from_file("path/to/openapi.yaml", module=endpoints)\n    \n### Client\n\n    from pyotr.client import Client\n    \n    client = Client.from_file("path/to/openapi.yaml")\n    result = client.some_endpoint_id("path", "variables", "query_var"="example")\n',
    'author': 'Berislav Lopac',
    'author_email': 'berislav@lopac.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pyotr.readthedocs.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
