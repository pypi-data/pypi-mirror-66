# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['springer']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.4.1,<0.5.0',
 'pandas>=1.0.3,<2.0.0',
 'requests>=2.23.0,<3.0.0',
 'typer>=0.1.1,<0.2.0',
 'xlrd>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['springer = springer.__main__:cli']}

setup_kwargs = {
    'name': 'springer',
    'version': '0.7.0',
    'description': 'Bulk Springer Textbook Downloader',
    'long_description': "# `springer`\n\nSpringer Textbook Bulk Download Tool\n\nNOTICE:\n\nAuthor not affiliated with Springer and this tool is not authorized\nor supported by Springer. Thank you to Springer for making these\nhigh quality textbooks available at no cost. \n\n**Usage**:\n\n```console\n$ springer [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `-L, --lang [en|de]`: Choose catalog language  [default: en]\n* `-C, --category [all|med]`: Choose a catalog catagory.  [default: all]\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `catalogs`: List available catalogs.\n* `clean`: Removes the cached catalog.\n* `download`: Download textbooks from Springer.\n* `list`: List textbooks in the catalog.\n* `refresh`: Refresh the cached catalog of Springer...\n\n## `springer catalogs`\n\nList available catalogs.\n\nLists all available collections in different languages.\n\n**Usage**:\n\n```console\n$ springer catalogs [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `springer clean`\n\nRemoves the cached catalog.\n    \n\n**Usage**:\n\n```console\n$ springer clean [OPTIONS]\n```\n\n**Options**:\n\n* `-F, --force`\n* `--all`\n* `--help`: Show this message and exit.\n\n## `springer download`\n\nDownload textbooks from Springer.\n\nThis command will download all the textbooks found in the catalog\nof free textbooks provided by Springer. The default file format \nis PDF and the files are saved by default to the current working\ndirectory.\n\nIf a download is interrupted, you can re-start the download and it\nwill skip over files that have been previously downloaded and pick up\nwhere it left off. \n\nIf the --all option is specified, the --dest=path option specifies the\nroot directory where files will be stored. Each catalog will save \nit's textbooks to:\n\ndest_path/language/category/book_file_name.fmt\n\n\nEXAMPLES\n\nDownload all books in PDF format to the current directory:\n\n$ springer download\n\nDownload all books in EPUB format to the current directory:\n\n$ springer download --format epub\n\nDownload all books in PDF format to a directory `pdfs`:\n\n$ springer download --dest-path pdfs\n\nDownload books in PDF format to `pdfs` with overwriting:\n\n$ springer download --dest-path pdfs --over-write\n\nDownload all books in PDF from the Germal all disciplines catalog:\n\n$ springer -L de -C all download --dest-path german/all/pdfs\n\n**Usage**:\n\n```console\n$ springer download [OPTIONS]\n```\n\n**Options**:\n\n* `-d, --dest-path PATH`: Destination directory for downloaded files.  [default: /Users/ejo/local/springer]\n* `-f, --format [pdf|epub]`: [default: pdf]\n* `-W, --over-write`: Over write downloaded files.  [default: False]\n* `--all`: Downloads books from all catalogs.\n* `--help`: Show this message and exit.\n\n## `springer list`\n\nList textbooks in the catalog.\n    \n\n**Usage**:\n\n```console\n$ springer list [OPTIONS]\n```\n\n**Options**:\n\n* `-f, --format [pdf|epub]`: [default: pdf]\n* `-p, --show-path`: Show generated filename for each book.\n* `--help`: Show this message and exit.\n\n## `springer refresh`\n\nRefresh the cached catalog of Springer textbooks.\n\nIf --all is specified, the --url option is ignored.\n\nExamples\n\nUpdate English language catalog:\n\n$ springer --language en refresh\n\nUpdate German language catalog whose category is 'all':\n\n$ springer --language de --category all refresh\n\nUpdate German language catalog whose category is 'med' with a new URL:\n\n$ springer -L de -C med refresh --url https://example.com/api/endpoint/something/v11\n\nUpdate all catalogs:\n\n$ springer refresh --all\n\n**Usage**:\n\n```console\n$ springer refresh [OPTIONS]\n```\n\n**Options**:\n\n* `-u, --url TEXT`: URL for Excel-formatted catalog\n* `--all`\n* `--help`: Show this message and exit.\n",
    'author': 'JnyJny',
    'author_email': 'erik.oshaughnessy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/JnyJny/springer_downloader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
