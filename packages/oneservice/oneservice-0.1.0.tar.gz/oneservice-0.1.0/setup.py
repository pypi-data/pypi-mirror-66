# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oneservice']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.1.2,<2.0.0']

entry_points = \
{'console_scripts': ['check = tasks:check',
                     'flake8 = tasks:flake8',
                     'mypy = tasks:mypy',
                     'test = tasks:test']}

setup_kwargs = {
    'name': 'oneservice',
    'version': '0.1.0',
    'description': '',
    'long_description': '# OneService\n\nWrapper around Flask aimed at conveniently creating microservices.\n\nFeatures and limitations:\n- `Microservice` creates a server that can call a handler method when `/` is hit (HTTP method is configurable)\n- The handler method receives the request JSON data and must respond with a `(dict, int)` tuple containing\nthe response data and response status code\n\n## Usage\n```python\nfrom oneservice import Microservice\n\ndef return_doubled(json_data: dict) -> (dict, int):\n    return {"result": int(json_data["a"]) * 2}, 200\n\nm = Microservice(handler=return_doubled)\nm.start()\n```\n\nYou may then hit the microservice and its health endpoint:\n```bash\ncurl http://localhost:5000/health\ncurl -X POST -H "Content-Type: application/json" --data \'{"a": 2}\' http://localhost:5000/\n```\n\nSee [/examples](examples) for more code usage samples.\n',
    'author': 'Davide Vitelaru',
    'author_email': 'davide@vitelaru.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/davidevi/oneservice',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
