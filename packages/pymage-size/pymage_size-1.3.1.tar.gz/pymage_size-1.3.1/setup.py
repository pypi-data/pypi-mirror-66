# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymage_size']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymage-size',
    'version': '1.3.1',
    'description': 'A Python package for getting the dimensions of an image without loading it into memory.',
    'long_description': '# pymage_size\nA Python package for getting the dimensions of an image without loading it into memory. No external dependencies either!\n\n## Disclaimer\nThis library is currently in Beta. This means that the interface might change and that not all possible edge cases have been properly tested.\n\n## Installation\npymage_size is available from PyPI, so you can install via `pip`:\n```bash\n$ pip install pymage_size\n```\n\n## Usage\n```python\nfrom pymage_size import get_image_size\n\nimg_format = get_image_size("example.png")\nwidth, height = img_format.get_dimensions()\n```\n',
    'author': 'CobaltCore',
    'author_email': 'cobaltcore@yandex.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kobaltcore/pymage_size',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
