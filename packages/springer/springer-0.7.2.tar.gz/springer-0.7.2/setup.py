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
    'version': '0.7.2',
    'description': 'Bulk Springer Textbook Downloader',
    'long_description': '# `springer`\n\nSpringer Textbook Bulk Download Tool\n\nNOTICE:\n\nAuthor not affiliated with Springer and this tool is not authorized\nor supported by Springer. Thank you to Springer for making these\nhigh quality textbooks available at no cost. \n\nFrom `https://www.springernature.com/gp/librarians/news-events/all-news-articles/industry-news-initiatives/free-access-to-textbooks-for-institutions-affected-by-coronaviru/17855960`:\n\n"With the Coronavirus outbreak having an unpretextbookscedented\nimpact on education, Springer Nature is launching a global program\nto support learning and teaching at higher education institutions\nworldwide. Remote access to educational resources has become\nessential. We want to support lecturers, teachers and students\nduring this challenging period and hope that this initiative will go\nsome way to help. \n\nInstitutions will be able to access more than 500 key textbooks\nacross Springer Nature’s eBook subject collections for free. In\naddition, we are making a number of German-language Springer medical\ntraining books on emergency nursing freely accessible.  These books\nwill be available via SpringerLink until at least the end of July."\n\nThis tool automates the tasks of downloading the Excel-formatted\ncatalogs and downloading the files described in the catalog.\n\n**Usage**:\n\n```console\n$ springer [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `-L, --lang [en|de]`: Choose catalog language  [default: en]\n* `-C, --category [all|med]`: Choose a catalog catagory.  [default: all]\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `catalogs`: List available catalogs.\n* `clean`: Removes the cached catalog.\n* `download`: Download textbooks from Springer.\n* `list`: List titles of textbooks in the catalog.\n* `refresh`: Refresh the cached catalog of Springer...\n\n## `springer catalogs`\n\nList available catalogs.\n    \n\n**Usage**:\n\n```console\n$ springer catalogs [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `springer clean`\n\nRemoves the cached catalog.\n    \n\n**Usage**:\n\n```console\n$ springer clean [OPTIONS]\n```\n\n**Options**:\n\n* `-F, --force`\n* `--all`\n* `--help`: Show this message and exit.\n\n## `springer download`\n\nDownload textbooks from Springer.\n\nThis command will download all the textbooks found in the catalog\nof free textbooks provided by Springer. The default file format \nis PDF and the files are saved by default to the current working\ndirectory.\n\nIf a download is interrupted, you can re-start the download and it\nwill skip over files that have been previously downloaded and pick up\nwhere it left off. \n\nIf the --all option is specified, the --dest-path option specifies the\nroot directory where files will be stored. Each catalog will save \nit\'s textbooks to:\n\ndest_path/language/category/book_file_name.fmt\n\nFiles that fail to download will be logged to a file named:\n\ndest_path/DOWNLOAD_ERRORS.txt\n\nThe log entries will have the date and time of the attempt,\nthe HTTP status code and the URL that was attempted.\n\n\nEXAMPLES\n\nDownload all books in PDF format to the current directory:\n\n$ springer download\n\nDownload all books in EPUB format to the current directory:\n\n$ springer download --format epub\n\nDownload all books in PDF format to a directory `pdfs`:\n\n$ springer download --dest-path pdfs\n\nDownload books in PDF format to `pdfs` with overwriting:\n\n$ springer download --dest-path pdfs --over-write\n\nDownload all books in PDF from the German all disciplines catalog:\n\n$ springer -L de -C all download --dest-path german/all/pdfs\n\nDownload all books from all catelogs in epub format:\n\n$ springer download --all --dest-path books --format epub\n\n**Usage**:\n\n```console\n$ springer download [OPTIONS]\n```\n\n**Options**:\n\n* `-d, --dest-path PATH`: Destination directory for downloaded files.  [default: /Users/ejo/local/springer]\n* `-f, --format [pdf|epub]`: [default: pdf]\n* `-W, --over-write`: Over write downloaded files.  [default: False]\n* `--all`: Downloads books from all catalogs.\n* `--help`: Show this message and exit.\n\n## `springer list`\n\nList titles of textbooks in the catalog.\n\nExamples\n\nList titles available in the default catalog (en-all):\n\n$ springer list\n\nList titles available in the German language, all disciplines catalog:\n\n$ springer --language de --category all list\n\n**Usage**:\n\n```console\n$ springer list [OPTIONS]\n```\n\n**Options**:\n\n* `-f, --format [pdf|epub]`: [default: pdf]\n* `-p, --show-path`: Show generated filename for each book.\n* `--help`: Show this message and exit.\n\n## `springer refresh`\n\nRefresh the cached catalog of Springer textbooks.\n\nIf --all is specified, the --url option is ignored.\n\nExamples\n\nUpdate English language catalog:\n\n$ springer --language en refresh\n\nUpdate German language catalog whose category is \'all\':\n\n$ springer --language de --category all refresh\n\nUpdate German language catalog whose category is \'med\' with a new URL:\n\n$ springer -L de -C med refresh --url https://example.com/api/endpoint/something/v11\n\nUpdate all catalogs:\n\n$ springer refresh --all\n\n**Usage**:\n\n```console\n$ springer refresh [OPTIONS]\n```\n\n**Options**:\n\n* `-u, --url TEXT`: URL for Excel-formatted catalog\n* `--all`\n* `--help`: Show this message and exit.\n',
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
