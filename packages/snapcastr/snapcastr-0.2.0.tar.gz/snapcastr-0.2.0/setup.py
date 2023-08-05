# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snapcastr']

package_data = \
{'': ['*'], 'snapcastr': ['static/*', 'templates/*']}

install_requires = \
['Flask>=1.1.2,<2.0.0',
 'flask-bootstrap>=3.3.7,<4.0.0',
 'flask-nav>=0.6,<0.7',
 'snapcast>=2.1.0,<3.0.0',
 'wtforms>=2.2.1,<3.0.0',
 'xdg>=4.0.1,<5.0.0']

entry_points = \
{'console_scripts': ['snapcastrd = snapcastr.snapcastrd:main']}

setup_kwargs = {
    'name': 'snapcastr',
    'version': '0.2.0',
    'description': 'webinterface to control a snapcast server',
    'long_description': "# snapcastr\n\n Snapcastr is a webinterface to control a [snapcast](https://github.com/badaix/snapcast/) server.\n\n It is written in python with flask, wtforms and python-snapcast\n\n- [python 3](https://www.python.org/)\n- [flask](http://flask.pocoo.org/)\n- [wtforms](https://wtforms.readthedocs.io)\n- [python-snapcast]( https://github.com/happyleavesaoc/python-snapcast)\n\n\n## getting started\n\n### install requirements\n\nuse your package manager, e.g. apt or pacman and install\n\n- python3\n- poetry\n\n### install\n\n#### get source\n\n```bash\n$ git clone https://github.com/xkonni/snapcastr\n```\n\n#### install locally\n\n```bash\n$ cd snapcastr\n$ poetry install\n```\n\n#### install system-wide\n\n```bash\n$ cd snapcastr\n$ poetry build\n$ sudo pip3 install dist/snapcastr-0.1.0.tar.gz\n```\n\n\n## run/debug\n### run\n\nshow help\n\n```bash\n$ snapcastrd -h\n\nusage: snapcastrd [-h] [--host host] [--port port] [--sc_host sc_host] [-c CONFIG] [-d]\n\nsnapcastr\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --host host           webinterface host\n  --port port, -p port  webinterface port\n  --sc_host sc_host, -s sc_host\n                        snapcast host\n  -c CONFIG, --config CONFIG\n                        config file\n  -d, --debug           debug mode\n\n\n```\n\nrun the application\n\n- when installed locally\n\n```bash\n$ cd snapcastr\n$ poetry run snapcastrd --sc_host=address_of_your_snapserver\n```\n\n- when installed system-wide\n\n```bash\n$ snapcastrd --sc_host=address_of_your_snapserver\n```\n\nThe `address_of_your_snapserver` might be 127.0.0.1 or localhost, if you are running\nsnapcastr on the same machine as your snapserver. Snapcastr doesn't need to run with super\nuser privileges (so you don't need to run it with `sudo`).\n\nBe aware that the last used configuration is saved in `$HOME/.config/snapcastr.json`.\n\n### debug\n\nto debug the application\n\n- when installed locally\n\n```bash\n$ cd snapcastr\n$ poetry run snapcastrd -d [other-options]\n```\n\n- when installed system-wide\n\n```bash\n$ snapcastrd -d [other-options]\n```\n\n\n## use\n\nOpen http://localhost:5011 in your browser.\n\n\n## features\n\n### main screen\n* View general status, number of clients, streams, groups of clients\n![main](https://github.com/xkonni/snapcastr/blob/master/doc/main.png)\n\n### clients\n* View connected clients and change their volume\n![clients](https://github.com/xkonni/snapcastr/blob/master/doc/clients.png)\n\n### groups\n* View the groups and the stream being played by each group\n![groups](https://github.com/xkonni/snapcastr/blob/master/doc/groups.png)\n\n### streams\n* View the status of the various streams available\n![streams](https://github.com/xkonni/snapcastr/blob/master/doc/streams.png)\n\n\n\n## roadmap, in no particular order\n\n### clients\n* rename\n* remove old\n\n### groups\n* rename\n* remove\n* add\n\n### streams\n* rename\n",
    'author': 'xkonni',
    'author_email': 'konstantin.koslowski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xkonni/snapcastr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
