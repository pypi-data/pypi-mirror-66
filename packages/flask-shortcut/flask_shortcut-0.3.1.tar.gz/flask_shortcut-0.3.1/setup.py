# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_shortcut', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'flask>=1.1.2,<2.0.0',
 'importlib-metadata>=1.6.0,<2.0.0',
 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'flask-shortcut',
    'version': '0.3.1',
    'description': 'Extension that provides an easy way to add dev-only shortcuts to your routes.',
    'long_description': '|Logo|\n\n|CI_CD| |pyPI| |Docs| |License| |py_versions| |Style|\n\n\n.. header-end\n\nProject Description\n-------------------\n\nThis extension provides an easy and safe way to add dev-only shortcuts to\nroutes in your flask application.\n\nThe main beneficiaries are microservices that need to be tested regularly in\nconjunction with their clients. If you need to assert working communication and\nbasic integration in a sufficiently complex ecosystem, clients that can not\nfreely chose how their requests are formed gain a lot from being able to\nreceive predictable responses. By skipping over the details of how the\nmicroservice is implemented, which bugs and minor changes it experiences over\ntime, testing basic API compatibility gets a lot more manageable.\n\n\n\nUsage\n-----\n\nYou can add shortcuts to your route functions either individually with\ndecorators, or in a single swoop once all routes have been defined. Both ways\nare functionally equivalent.\n\n**With decorators:**\n\n.. code-block:: python\n\n    from flask import Flask\n    from flask_shortcut import Shortcut\n\n    app = Flask(__name__)\n    short = Shortcut(app)\n\n    app.route(\'/foo\', methods=[\'GET\'])\n    short.cut((\'short_foo\', 200))\n    def foo():\n        return \'foo\'\n\n    app.route(\'/bar\', methods=[\'POST\'])\n    short.cut({\'{"name": "TestUser"}\': (\'short_bar\', 200)})\n    def bar():\n        return \'bar\'\n\n**With a wire call**\n\n.. code-block:: python\n\n    from flask import Flask\n    from flask_shortcut import Shortcut\n\n    app = Flask(__name__)\n\n    app.route(\'/foo\', methods=[\'GET\'])\n    def foo():\n        return \'foo\'\n\n    app.route(\'/bar\', methods=[\'POST\'])\n    def bar():\n        return \'bar\'\n\n    Shortcut(app).wire(\n        {\n             \'/foo\': (\'short_foo\', 200),\n             \'/bar\': {\'{"name": "TestUser"}\': (\'short_bar\', 200)\n        }\n    )\n\n\n----\n\nProject home `on github`_.\n\n.. |Logo| image:: https://user-images.githubusercontent.com/2063412/79608525-76ff3100-80f5-11ea-9421-a7e0b7a20ac2.png\n   :alt: Logo\n   :width: 1200\n   :target: https://github.com/a-recknagel/Flask-Shortcut\n\n.. |CI_CD| image:: https://github.com/a-recknagel/Flask-Shortcut/workflows/CI-CD/badge.svg\n   :alt: Main workflow status\n   :target: https://github.com/a-recknagel/Flask-Shortcut/actions\n\n.. |pyPI| image:: https://img.shields.io/pypi/v/flask-shortcut\n   :alt: Current pyPI version\n   :target: https://pypi.org/project/flask-shortcut/\n\n.. |Docs| image:: https://img.shields.io/badge/docs-github--pages-blue\n   :alt: Documentation home\n   :target: https://a-recknagel.github.io/Flask-Shortcut/\n\n.. |License| image:: https://img.shields.io/pypi/l/flask-shortcut\n   :alt: Package license\n   :target: https://pypi.org/project/flask-shortcut/\n\n.. |py_versions| image:: https://img.shields.io/pypi/pyversions/flask-shortcut\n   :alt: Supported on python versions\n   :target: https://pypi.org/project/flask-shortcut/\n\n.. |Style| image:: https://img.shields.io/badge/codestyle-black-black\n   :alt: Any color you want\n   :target: https://black.readthedocs.io/en/stable/\n\n.. _on github: https://github.com/a-recknagel/Flask-Shortcut',
    'author': 'Arne',
    'author_email': 'arecknag@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/a-recknagel/Flask-Shortcut',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
