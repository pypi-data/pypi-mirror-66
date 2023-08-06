# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mapling']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.3,<2.0.0',
 'requests>=2.23.0,<3.0.0',
 'spacy>=2.2.4,<3.0.0',
 'textract>=1.6.3,<2.0.0',
 'typer[all]>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['mapling = mapling.main:app']}

setup_kwargs = {
    'name': 'mapling',
    'version': '0.1.1',
    'description': '',
    'long_description': '<h1><img src="https://image.flaticon.com/icons/png/512/40/40054.png" width="120px"><br>mapling</h1>\n\nMapling finds things, such as place names, in texts.  It returns a csv file with a row for each occurence. For each file, it creates an html page with the things highlighted.  Just point mapling to a folder full of documents. Mapling uses [textract](https://textract.readthedocs.io/en/latest/) to extract text from many types of files, including csv, doc, docx, pdf, html, txt and many others.\n\nUsage: `$ mapling texts/  --gazetteer=gazetteer/gazetteer.txt --model=de_core_news_sm --html`\nTo install a [spaCy model](https://spacy.io/models): `$ python -m spacy download de_core_news_sm`\n\n- The first approach is to use a gazetteer. Mapling expects a txt file with a row for each place name.\nAdd the `--gazetter` argument with the path to your file. This approach lets you search for specific terms (not just places) that appear in the text.\n`$ mapling /dir/with/txt_files --gazetteer="/home/me/gazetter.txt"`\n\n- The second approach uses a spaCy named entity recognition model.  Add the `--model` argument with\nthe name of an installed spaCy model.  If your model is not installed or does not\nhave an ner pipeline, you\'ll get instructions on how to fix that. This approach will return a large range of entities and places, more than you might list yourself.  This is useful for establishing which places, people and organizations appear in a text.\n`$ mapling /dir/with/txt_files  --model=de_core_news_md`\n\n\n- Finally, mapling can create visualizations.  Add the `--html` argument\n`$ mapling /dir/with/txt_files  --model=de_core_news_md --html`\n\nTo install:\n```\npip install mapling\n```\n\nIn the future, mapling will also work with the [Word Historical Gazetteer](http://dev.whgazetteer.org/) to rectify, geocode and map your place names.\n',
    'author': 'Andrew Janco',
    'author_email': 'ajanco@haverford.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
