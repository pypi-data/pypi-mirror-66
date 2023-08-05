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
    'version': '0.8.0',
    'description': 'Bulk Springer Textbook Downloader',
    'long_description': '# `springer`\n\nSpringer Textbook Bulk Download Tool\n\n**NOTICE**:\n\nAuthor not affiliated with Springer and this tool is not authorized\nor supported by Springer. Thank you to Springer for making these\nhigh quality textbooks available at no cost. \n\n\x08\n>"With the Coronavirus outbreak having an unprecedented impact on\n>education, Springer Nature is launching a global program to support\n>learning and teaching at higher education institutions\n>worldwide. Remote access to educational resources has become\n>essential. We want to support lecturers, teachers and students\n>during this challenging period and hope that this initiative will go\n>some way to help.\n>\n>Institutions will be able to access more than 500 key textbooks\n>across Springer Nature’s eBook subject collections for free. In\n>addition, we are making a number of German-language Springer medical\n>training books on emergency nursing freely accessible.  These books\n>will be available via SpringerLink until at least the end of July."\n\n[Source](https://www.springernature.com/gp/librarians/news-events/all-news-articles/industry-news-initiatives/free-access-to-textbooks-for-institutions-affected-by-coronaviru/17855960)\n\nThis tool automates the tasks of downloading the Excel-formatted\ncatalogs and downloading the files described in the catalog.\n\nThis utility can be installed using `pip`:\n\n`$ python3 -m pip install springer`\n\nOr the latest from master:\n\n`$ python3 -m pip install git+https://github.com/JnyJny/springer_downloader`\n\nThe source is available on [GitHub](https://github.com/JnyJny/springer_downloader).\n\n**Usage**:\n\n```console\n$ springer [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `-L, --lang [en|de]`: Choose catalog language  [default: en]\n* `-D, --description [all|med]`: Choose a catalog description.  [default: all]\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `clean`: Removes the cached catalog.\n* `download`: Download textbooks from Springer.\n* `list`: List books, package, packages, catalog or...\n* `refresh`: Refresh the cached catalog of Springer...\n\n## `springer clean`\n\nRemoves the cached catalog.\n\nExamples\n\nRemove the English language, all disciplines cached catalog:\n\n`$ springer clean --force`\n\nRemove the German language emergency nursing cached catalog:\n\n`$ springer -L de -D med clean --force`\n\nRemove all catalogs:\n\n`$ springer clean --force --all`\n\n**Usage**:\n\n```console\n$ springer clean [OPTIONS]\n```\n\n**Options**:\n\n* `-F, --force`\n* `--all`\n* `--help`: Show this message and exit.\n\n## `springer download`\n\nDownload textbooks from Springer.\n\nThis command will download all the textbooks found in the catalog\nof free textbooks provided by Springer. The default file format \nis PDF and the files are saved by default to the current working\ndirectory.\n\nIf a download is interrupted, you can re-start the download and it\nwill skip over files that have been previously downloaded and pick up\nwhere it left off. \n\nIf the --all option is specified, the --dest-path option specifies the\nroot directory where files will be stored. Each catalog will save \nit\'s textbooks to:\n\ndest_path/language/description/book_file_name.fmt\n\nFiles that fail to download will be logged to a file named:\n\ndest_path/DOWNLOAD_ERRORS.txt\n\nThe log entries will have the date and time of the attempt,\nthe HTTP status code and the URL that was attempted.\n\n\nEXAMPLES\n\nDownload all books in PDF format to the current directory:\n\n`$ springer download`\n\nDownload all books in EPUB format to the current directory:\n\n`$ springer download --format epub`\n\nDownload all books in PDF format to a directory `pdfs`:\n\n`$ springer download --dest-path pdfs`\n\nDownload books in PDF format to `pdfs` with overwriting:\n\n`$ springer download --dest-path pdfs --over-write`\n\nDownload all books in PDF from the German/All_Disciplines catalog:\n\n`$ springer -L de -D all download --dest-path german/all/pdfs`\n\nDownload all books from all catelogs in epub format:\n\n`$ springer download --all --format epub`\n\nDownload all books in the \'Computer Science\' package in pdf format:\n\n`$ springer download -p Computer`\n\n**Usage**:\n\n```console\n$ springer download [OPTIONS]\n```\n\n**Options**:\n\n* `-p, --package-name TEXT`: Package name to match (partial name OK).\n* `-f, --format [pdf|epub]`: [default: pdf]\n* `-d, --dest-path PATH`: Destination directory for downloaded files.  [default: /Users/ejo/local/springer]\n* `-W, --over-write`: Over write downloaded files.  [default: False]\n* `--all`: Downloads books from all catalogs.\n* `--help`: Show this message and exit.\n\n## `springer list`\n\nList books, package, packages, catalog or catalogs,\n\nExamples\n\nList titles available in the default catalog:\n\n`$ springer list books`\n\nList packages available in the default catalog:\n\n`$ springer list packages`\n\nList titles available in the German language, all disciplines catalog:\n\n`$ springer --language de --description all list books`\n\nList all eBook packages in the default catalog:\n\n`$ springer list packages`\n\nList all eBook packages in the default catalog whose name match:\n\n`$ springer list package -m science`\n\nList information about the current catalog:\n\n`$ springer list catalog`\n\nList information about the Germal language, Emergency Nursing catalog:\n\n`$ springer --language de --description med list catalog`\n\n**Usage**:\n\n```console\n$ springer list [OPTIONS] [catalogs|catalog|packages|package|books]\n```\n\n**Options**:\n\n* `-m, --match TEXT`: String used for matching.\n* `-l, --long-format`: Display selected information in a longer format.  [default: False]\n* `--help`: Show this message and exit.\n\n## `springer refresh`\n\nRefresh the cached catalog of Springer textbooks.\n\nIf --all is specified, the --url option is ignored.\n\nExamples\n\nUpdate English language catalog:\n\n`$ springer --language en refresh`\n\nUpdate German language catalog whose description is \'all\':\n\n`$ springer --language de --description all refresh`\n\nUpdate German language catalog whose description is \'med\' with a new URL:\n\n`$ springer -L de -D med refresh --url https://example.com/api/endpoint/something/v11`\n\nUpdate all catalogs:\n\n`$ springer refresh --all`\n\n**Usage**:\n\n```console\n$ springer refresh [OPTIONS]\n```\n\n**Options**:\n\n* `-u, --url TEXT`: URL for Excel-formatted catalog\n* `--all`\n* `--help`: Show this message and exit.\n',
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
