# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.pelican_jupyter_reader']

package_data = \
{'': ['*']}

install_requires = \
['nbconvert>=5.6.1,<6.0.0', 'nbformat>=4.4.0,<5.0.0', 'pelican>=4.2,<5.0']

extras_require = \
{'markdown': ['markdown>=3.1.1,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-jupyter-reader',
    'version': '0.3.1',
    'description': 'Reader for ipynb files',
    'long_description': '`pelican-jupyter-reader`: A Plugin for Pelican\n---------------------------------------------\n\n[![PyPI version](https://badge.fury.io/py/pelican-jupyter-reader.svg)](https://badge.fury.io/py/pelican-jupyter-reader)\n[![Netlify Status](https://api.netlify.com/api/v1/badges/a92deaef-8ffb-4d11-a941-358ac92e3500/deploy-status)](https://app.netlify.com/sites/peaceful-jang-e394ce/deploys)\n\nThis [Pelican](http://docs.getpelican.com/en/latest/index.html) plugin provides a Jupyter Notebook (i.e. `*.ipynb`) reader.\nThe plugin intends to allow users to simply drop Jupyter notebooks in their\nPelican content directory and have the notebooks rendered (beautifully) in a Pelican\nstatic website.\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    pip install pelican-jupyter-reader\n\nQuickstart\n----------\n\n- Add the plugin to `pelicanconf.py`:\n```python\n# ...\n\nfrom pelican.plugins import pelican_jupyter_reader\nPLUGINS = [pelican_jupyter_reader]\n\n# ...\n```\n\n- Provide [Pelican post\n  metadata](http://docs.getpelican.com/en/latest/content.html#file-metadata) as\n  a top-level object with key `pelican` in the Jupyter notebook metadata:\n```javascript\n{\n    "pelican": {\n        "date": "2020-04-10",\n        "title": "this is a title",\n        "tags": "thats, awesome",\n        "category": "yeah",\n        "slug": "my-super-post",\n        "authors": "Alexis Metaireau, Conan Doyle",\n        "summary": "Short version for index and feeds"\n    },\n    "kernelspec": {\n        "display_name": "Python 3",\n        "language": "python",\n        "name": "python3"\n    },\n//...the rest of the notebook JSON follows.\n```\n\n- Drop your Jupyter notebook in the Pelican content directory, build your site,\n  and deploy!  :rocket:\n\n\nExample\n-------\n\nThe [demo/](https://github.com/chuckpr/pelican-jupyter-reader/tree/master/demo)\ndirectory has a simple post with corresponding configuration in\n`pelicanconf.py`. The demo site is deployed\n[here](https://peaceful-jang-e394ce.netlify.app).\n\n\nNotes\n-----\n\nThe Jupyter nbconvert configuration for\n[preprocessors](https://github.com/jupyter/nbconvert/tree/5.x/nbconvert/preprocessors)\nand the\n[HTMLExporter](https://github.com/jupyter/nbconvert/blob/5.x/nbconvert/exporters/html.py)\nare exposed in your Pelican config, `pelicanconf.py`.  This\nmeans you can manipulate notebooks with utilities provided by `nbconvert`.\n\nFor example, to use the `basic` template for the `HTMLExporter`, you could add\nthe following to your `pelicanconf.py`:\n\n```python\nfrom traitlets.config import Config\nNBCONVERT_CONFIG = Config()\nNBCONVERT_CONFIG.HTMLExporter.template = \'basic\'\n```\n\nTo strip empty cells from the notebook before publishing, you might add this\noption to `pelicanconf.py`:\n\n```python\n# ...\nNBCONVERT_CONFIG.RegexRemovePreprocessor.patterns = [\'\\\\s*\\\\Z\']\n```\n\nOther `nbconvert` configuration options can be found\n[here](https://nbconvert.readthedocs.io/en/latest/config_options.html#configuration-options).\n',
    'author': 'Chuck Pepe-Ranney',
    'author_email': 'chuck.peperanney@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chuckpr/pelican-jupyter-reader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
