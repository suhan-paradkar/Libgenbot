import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'Libgenbot',
  packages = setuptools.find_packages(),
  version = '1.0.0-alpha-02',
  license='GPL-3.0',
  description = 'Libgenbot is a Python tool for downloading articles from Libgen, inspired by PyPaperBot.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Suhan G Paradkar',
  author_email = 'suhangp2002@gmail.com',
  url = 'https://github.com/suhan-paradkar/Libgenbot',
  download_url = 'https://github.com/suhan-paradkar/Libgenot/archive/v1.0.0-alpha.tar.gz',
  keywords = ['download-papers','google-scholar', 'libgen', 'scihub', 'scholar', 'crossref', 'papers'],
  install_requires=[
        'astroid>=2.4.2,<=2.5',
        'beautifulsoup4>=4.9.1',
        'bibtexparser>=1.2.0',
        'certifi>=2020.6.20',
        'chardet>=3.0.4',
        'colorama>=0.4.3',
        'crossref-commons>=0.0.7',
        'future>=0.18.2',
        'HTMLParser>=0.0.2',
        'idna>=2.10,<3',
        'isort>=5.4.2',
        'lazy-object-proxy>=1.4.3',
        'mccabe>=0.6.1',
        'numpy',
        'pandas',
        'pyChainedProxy>=1.1',
        'pylint>=2.6.0',
        'pyparsing>=2.4.7',
        'python-dateutil>=2.8.1',
        'pytz>=2020.1',
        'ratelimit>=2.2.1',
        'requests>=2.24.0',
        'six>=1.15.0',
        'soupsieve>=2.0.1',
        'toml>=0.10.1',
        'urllib3>=1.25.10',
        'wrapt>=1.12.1',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
  entry_points={
    'console_scripts': ["Libgenbot=Libgenbot.__main__:main"],
  },
)
