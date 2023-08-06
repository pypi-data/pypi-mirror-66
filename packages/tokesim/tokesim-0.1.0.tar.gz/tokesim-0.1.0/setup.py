# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tokesim',
 'tokesim.agents',
 'tokesim.client',
 'tokesim.commands',
 'tokesim.config',
 'tokesim.models',
 'tokesim.simulation',
 'tokesim.template',
 'tokesim.template.ethereum',
 'tokesim.template.ethereum.contracts',
 'tokesim.util',
 'tokesim.visualizations']

package_data = \
{'': ['*']}

install_requires = \
['humps>=0.2.2,<0.3.0',
 'jsonschema>=3.2.0,<4.0.0',
 'mesa-behaviors>=0.1.0,<0.2.0',
 'mesa>=0.8.6,<0.9.0',
 'mypy_extensions>=0.4.3,<0.5.0',
 'numpy>=1.18.2,<2.0.0',
 'requests>=2.23.0,<3.0.0',
 'web3>=5.7.0,<6.0.0']

entry_points = \
{'console_scripts': ['toke = tokesim.__main__:main',
                     'tokesim = tokesim.__main__:main']}

setup_kwargs = {
    'name': 'tokesim',
    'version': '0.1.0',
    'description': 'A tool for building shareable Multi-Agent tokenomic models',
    'long_description': '# Tokesim \n![CI](https://github.com/tokesim/tokesim/workflows/CI/badge.svg)\n<center>\n  <h3 align="center">Tokesim</h3>\n\n  <p align="center">\n    A Tokeneconomics Simulator.\n    <br />\n    <a href="https://youtube.com/">View Demo</a>\n    ·\n    <!-- <a href="https://github.com/tokesim/issues/new?assignees=&labels=&template=bug_report.md&title=">Report Bug</a>-->\n    ·\n    <!-- <a href="https://github.com/tokesim/issues/new?assignees=&labels=&template=feature_request.md&title=">Request Feature</a> -->\n  </p>\n</center>\n\n<!-- table of contents -->\n## Table of Contents\n  - [About The Project](#about-the-project)\n  - [Getting Started](#getting-started)\n      - [Prerequisites](#prerequisites)\n      - [Installation](#installation)\n- [Usage](#usage)\n  - [Run Simulation](#run-simulation)\n  - [Start explorer](#start-the-explorer)\n  - [Configurations](#configurations)\n- [Contributing](#contributing)\n- [Resources](#resources)\n\n<!-- about the project -->\n## About The Project\n\n[Tokesim](https://tokesim.org) is an Agent Based Modeling tool that makes it easy to test token economic models. It\'s built using [mesa-behaviors](https://github.com/mesa_behaviors) an extension to [Mesa](https://github.com/mesaproject/mesa) ABM framework bring more type hints and patterns to make models,agents,utility functions and strategies shareable and more extensible.  The goal of Tokesim is to help developers run simulations against Smart Contracts, in a block chain agnostic way, using shreable and reusable modules and libraries to do so. \n\nTokesim Features:\n- Typehints to make agents and models extensible \n- Ability to run against and simulation against your smart contracts\n- An architecture to make the simulations portable to multiple chains\n- ChartJS integration from Mesa framework\n- Support for testing Ethereum based smart contracts directly\n\n\n<!-- getting started with the project -->\n## Getting Started\n### Prerequisites\n- node `v10.15.3` or later\n- npm `v6.4.1` or later\n- python `3.7` or later but not 3.8 ;) \n\n### Installation\nClone/ download the project, and install dependencies. For development\n```bash\ngit clone https://github.com/tokesim/tokesim.git && cd tokesim \npython3.7 -m venv venv\nsource venv/bin/activate\npip install poetry\npoetry build\nnpm install -g @tokesim/tokesim-chain\n# in a new terminal window\ntokesim-chain --port 5554\n```\nor \n```bash\npip install tokesim\nnpm install -g @tokesim/tokesim-chain\n# in a new terminal window\ntokesim-chain --port 3004\n```\n\n\n<!-- example usage, screen shots, demos -->\n## Usage\n### Run simulation \nIn order to run a simulation against a chain the default init will create a simulation for you to modify as you see fit. You\'ll need to start the chain simulation service.\n```bash\n# remember to activate your venv\nsource venv/bin/activate\npip install tokesim\n\n# just like create react app generate template\ntokesim init --dir simple-token --agents 20\n\n#start chain simulator\ntokesim-chain -c ethereum --port 3004\n\n#run the simulation defaults to terminating after 100 steps\ntokesim run --config ./simple-token/simulation.json --port 3004\n```\n\n#### Simulation App Layout \n\nBy default tokesim init will generate a default application layout, that specifies the accounts used a balance for each of the agents as well as configuration file and some simple bonded token curve agents. The contracts specified are a listed [here](https://github.com/tokesim/example-smart-contracts)\n\n```bash\n# ./simple-token/\n.\n└── simple-token    \n    └── contracts \n    |    |── SimpleToken.bin\n    |    └── SimpleToken_abi.json\n    |── accounts.json    \n    |── config_schema.json       \n    |── simple_token_agent.py\n    |── simple_token_model.py\n    |── simple_token_config.py\n    └── simulation.json\n```\n\n### Configurations\nExplanation coming soon\n<!-- template just leave alone  -->\n## Roadmap\nComing soon\n\n<!-- template just leave alone  -->\n## Contributing\nHow to contribute, build and release are outlined in [CONTRIBUTING.md](CONTRIBUTING.md), [BUILDING.md](BUILDING.md) and [RELEASING.md](RELEASING.md) respectively. Commits in this repository follow the [CONVENTIONAL_COMMITS.md](CONVENTIONAL_COMMITS.md) specification.\n\n## License\nApache License 2.0\n\n<!-- references and additional resources  -->\n## Resources\n- [Mesa](https://github.com/mesaproject/mesa)\n- [mesa-behaviors](https://github.com/tokesim/mesa_behaviors)\n- [tokesim-chain](https://github.com/tokesim/tokesim-chain)\n- [OpenRPC](https://open-rpc.org)\n',
    'author': 'Zane Starr',
    'author_email': 'zcstarr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tokesim/mesa_behaviors',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
