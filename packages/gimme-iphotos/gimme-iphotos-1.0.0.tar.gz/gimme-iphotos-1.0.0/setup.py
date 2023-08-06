# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gimme_iphotos']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0', 'pyicloud>=0.9.6,<0.10.0', 'tqdm>=4.45.0,<5.0.0']

entry_points = \
{'console_scripts': ['gimme-iphotos = gimme-iphotos.cli:main']}

setup_kwargs = {
    'name': 'gimme-iphotos',
    'version': '1.0.0',
    'description': 'Download photos and videos from iCloud',
    'long_description': '# Gimme-iPhotos\n\nDownload media files from iCloud.\n\nThis tool uses [pyicloud] to synchronize photos and videos from iCloud to your\nlocal machine.\n\n## Features\n\n- Downloads media files from iCloud in parallel (might be beneficial on small files and wide bandwidth)\n- Keeps local collection in sync with iCloud by:\n  - skipping files which exist locally\n  - removing local files which were removed from the cloud\n- Reads configuration from ini-file\n- Stores password in keychain (provided by [pyicloud])\n- Supports two-factor authentication\n- Shows nice progress bars (thanks to [tqdm])\n\n## Usage\n\n```\n$ gimme-iphotos --help\nusage: gimme-iphotos [-h] [-c CONFIG] [-v] [-u USERNAME] [-p PASSWORD] [-d DESTINATION] [-o] [-r] [-n PARALLEL]\n\nDownload media files from iCloud\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -c CONFIG, --config CONFIG\n                        Configuration file\n  -v, --verbose\n  -u USERNAME, --username USERNAME\n  -p PASSWORD, --password PASSWORD\n  -d DESTINATION, --destination DESTINATION\n                        Destination directory\n  -o, --overwrite       Overwrite existing files\n  -r, --remove          Remove missing files\n  -n PARALLEL, --num-parallel-downloads PARALLEL\n```\n\n[pyicloud]: (https://github.com/picklepete/pyicloud)\n[tqdm]: (https://github.com/tqdm/tqdm)\n',
    'author': 'German Lashevich',
    'author_email': 'german.lashevich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Zebradil/Gimme-iPhotos',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
