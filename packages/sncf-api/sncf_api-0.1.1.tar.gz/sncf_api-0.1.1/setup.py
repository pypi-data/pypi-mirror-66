# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sncf_api']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.3,<2.0.0', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'sncf-api',
    'version': '0.1.1',
    'description': "A class of functions that can call the different SNCF API's from https://data.sncf.com/, returns data as pandas dataframe or .json() object.",
    'long_description': "# SNCF Api\n\n[![Build Status](https://travis-ci.com/matthew73210/sncf_api.svg?branch=master)](https://travis-ci.com/matthew73210/sncf_api)\n\n[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/matthew73210/sncf_api/?ref=repository-badge)\n\n[![CodeFactor](https://www.codefactor.io/repository/github/matthew73210/sncf_api/badge)](https://www.codefactor.io/repository/github/matthew73210/sncf_api)\n\nA class of methods that can call the different SNCF API's from [SNCF Open Data](https://data.sncf.com/), returns data as a [Pandas](https://pandas.pydata.org/) dataframe or .json() object.\n\nThat Pandas dataframe has some elements clipped.\n\nSome of the calls can be huge, as SNCF has put a lot of data up. Some calls may even max out the api interface. **list line** by type is an example.\n\n## Requirements\n\n- Pandas\n- Requests\n- Python 3.8\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install.\n\n```bash\npip install sncf-api\n```\n\n## Usage\n\nImport the class.\n\n```python\nimport sncf_api as sncf\n```\n\nCall the class (with or without the line code).\n\n```python\nsncf = sncf(903000)\n```\n\nOr\n\n```python\nsncf = sncf()\n```\n\nCall methods.\n\n```python\ndb = sncf.list_construction_site()\n```\n\nTo get a list of methods from class.\n\n```python\nhelp(sncf)\n```\n\n## Notes\n\nMethods don't need to be called with arguments, only the class.\nThe **convert_to_pandas_db()** method with used the data from the last method called and return a pandas dataframe.\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n\n## URL's\n\n[SNCF Open Data](https://data.sncf.com/)\n\n[Pandas](https://pandas.pydata.org/)\n\n[Pip](https://pip.pypa.io/en/stable/)\n\n[Make a readme](https://www.makeareadme.com/)\n",
    'author': 'Matthew Burton',
    'author_email': 'matthewmaxwellburton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matthew73210/sncf_api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
