# Libgenbot
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fsuhan-paradkar%2FLibgenbot&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![PyPI version](https://badge.fury.io/py/Libgenbot.svg)](https://badge.fury.io/py/Libgenbot)

Libgenbot is a Bot written in Python to download PDFs from libgen.
It is a fork of PyPaperBot, and is inspired by it
Please leave feedback and report issues

## Installation

Use pip to install LibgenBot

```
pip3 install Libgenbot
```

For builds with latest changes

```
git clone https://github.com/suhan-paradkar/Libgenbot.git
pip3 install -r requirements.txt
python3 setup.py install
```

## Installation in termux

First, you need to be subscribed into its-pointless repo

```
pkg up
pkg install wget git
wget https://its-pointless.github.io/setup-pointless-repo.sh
chmod +x setup-pointless-repo.sh
./setup-pointless-repo.sh
```

Now, you need to install numpy

```
pkg install numpy
```

Now, install pandas.... It takes a bit long time... so have a cup of tea

```
export CFLAGS="-Wno-deprecated-declarations -Wno-unreachable-code"
pip install pandas
```

Now, install using pip

```
pip install Libgenbot
```

For builds with latest changes

```
git clone https://github.com/suhan-paradkar/Libgenbot.git
pip install -r requirements.txt
python setup.py install
```

## Usage

| Arguments          | Description                                                                              | Type   |
| ------------------ | ---------------------------------------------------------------------------------------- | ------ |
| `--query`          | Query to make on Libgen page                                                             | string |
| `--genre`          | select genre: one of 'libgen(Sci-Tech)[1]''Scientific articles[2]' 'Fiction[3]' . Is a must when using libgen                      | Int |
| `--scholar-query`  | Query to be made on the Google Scholar page                                              | string |
| `--doi`            | DOI of the paper to download (this option uses only SciHub to download)                  | string |
| `--doi-file`       | File .txt containing the list of paper's DOIs to download                                | string |
| `--libgen-pages`   | Number or range of Libgen pages to inspect. Contains variable no. of pages               | string | 
| `--scholar-pages`  | Number or range of Google Scholar pages to inspect. Each page has a maximum of 10 papers | string |
| `--libgen-results` | Number of papers to download. Useful When \-\-libgen-pages=1                             | int    |
| `--scholar-results`| Number of papers to download. Useful When \-\-scholar-pages=1                            | int    | 
| `--dwn-dir`        | Directory path in which to save the result                                               | string |
| `--min-year`       | Minimal publication year of the paper to download                                        | int    |
| `--max-dwn-year`   | Maximum number of papers to download sorted by year                                      | int    |
| `--max-dwn-cites`  | Maximum number of papers to download sorted by number of citations                       | int    |
| `--journal-filter` | CSV file path of the journal filter . Only works on Scholar                              | string |
| `--restrict`       | 0:Download only Bibtex - 1:Down load only papers PDF                                     | int    |
| `--scihub-mirror`  | Mirror for downloading papers from sci-hub. If not set, it is selected automatically     | string |
| `--proxy`          | Use Proxychains. Provide a seperated list of proxies (See below)                         | string |
| `-h`               | Shows the help                                                                           | --     |

## Note

You can use only one of the arguments in the following groups

 `--query`, `--scholar-query` `--doi-file`, and `--doi` 
 `--max-dwn-year` and `and max-dwn-cites`

One of the arguments `--doi`, `--query`, `--scholar-query` , and `--file` is mandatory
The arguments `--scholar-pages` is mandatory when using `--scholar-query`
The argument `--dwn-dir` is mandatory.
The argument `--genre` is mandatory when using `--query`

The argument `--journal-filter`  require the path of a CSV containing a list of journal name paired with a boolean which indicates whether or not to consider that journal (0: don't consider /1: consider)

The argument `--doi-file`  require the path of a txt file containing the list of paper's DOIs to download organized with one DOI per line.

The argument `--proxy` must be used at the end of the command. The protocol used and the port must be mentioned. 

#### Usage of Proxy

```
Libgenbot --query=rheumatoid+arthritis --libgen-pages=1 --libgen-results=20 --genre=1 --dwn-dir=documents/ --proxy http://1.1.1.1:8080 http://8.0.8.0:8024
```
