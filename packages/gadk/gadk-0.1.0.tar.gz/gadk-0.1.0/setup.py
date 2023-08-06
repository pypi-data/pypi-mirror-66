# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gadk']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'pyyaml>=5.3,<6.0']

entry_points = \
{'console_scripts': ['gadk = gadk.cli:cmd']}

setup_kwargs = {
    'name': 'gadk',
    'version': '0.1.0',
    'description': 'Unofficial Github Actions Development Kit',
    'long_description': '# GADK\n\nThe extremely unofficial Github Actions Development Kit.\n\n## Features\n\n* Define Github Actions Workflows as Python.\n* Share common Workflow patterns, like build-test-deploy.\n* Abstract features like Artifacts.\n\n## Example\n\nBelow is a very simple example of generating a Workflow file. Take it with a grain of salt.\nGADK only shines when there are more workflows that look similar or share configuration.\n\nCreate a file called actions.py:\n\n```python3\nfrom gadk import *\n\n\nclass MyService(Workflow):\n    def __init__(self) -> None:\n        super().__init__("my_service", "my service workflow")\n\n        paths = [\n            "src/service/*.py",\n            "src/service.yml",\n        ]\n        self.on(\n            pull_request=On(paths=paths), push=On(branches=["master"], paths=paths),\n        )\n\n        self.jobs["test"] = Job(\n            steps=[\n                RunStep("make build"),\n                RunStep("make lint"),\n                RunStep("make test"),\n            ],\n        )\n```\n\nRun `python gadk/cli.py`. You should see the following printed (soon to be written to a file):\n\n```yaml\nname: my service workflow\n\'on\':\n  pull_request:\n    paths:\n    - src/service/*.py\n    - src/service.yml\n  push:\n    paths:\n    - src/service/*.py\n    - src/service.yml\n    branches:\n    - master\njobs:\n  test:\n    runs-on: ubuntu-18.04\n    steps:\n    - uses: actions/checkout@v1\n    - run: make build\n    - run: make lint\n    - run: make test\n```\n\n## Roadmap\n\n* Feature completeness: the first version of `gadk` was created to scratch a limited itch.\nThe next step is to represent all possible workflows.\n* Validation: the configuration is not validated but elements like `workflow.on` are required.\nIn the future this could be validated using a Yaml schema validator and runtime checks, e.g. specifying\na non-existent job in `job.needs`.\n',
    'author': 'Maarten Jacobs',
    'author_email': 'maarten.j.jacobs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maartenJacobs/gadk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
