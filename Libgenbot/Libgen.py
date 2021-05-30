import time
import requests
from .HTMLparsers import LibgenParser
from .Crossref import getPapersInfo
from .NetInfo import NetInfo
import sys

def libgen_requests(libgen_pages, url, restrict, genre, libgen_results=25):
    to_download = []

    for i in libgen_pages:
        url += "&page="+str(i)
        html = requests.get(url, headers=NetInfo.HEADERS)
        htmlt = html.text
        lpapers = LibgenParser(htmlt, genre)
        print("\nLibgen page {} : {} papers found".format(i,libgen_results))

        if(len(lpapers)>0):
            to_download.append(lpapers)
        else:
            print("Paper not found...")
            sys.exit()

    return to_download

def LibgenPapersInfo(lquery, libgen_pages, genre, restrict, libgen_results=10):
    to_download = []
    if genre == 1:
        libgen_results_arg = 25

        if libgen_results > 25:
                libgen_results_arg += 25
                if libgen_results > 50:
                    libgen_results_arg += 50

        url = "https://libgen.is/search.php?req="+lquery+"&lg_topic=libgen&open=0&view=simple&res="+str(libgen_results_arg)+"&phrase=1&column=def"

    if genre == 2:
        url = "https://libgen.is/scimag/?q="+lquery

    if genre == 3:
        url = "https://libgen.is/fiction/?q="+lquery

    to_download = libgen_requests(libgen_pages, url, restrict, genre, libgen_results)


    return [item for sublist in to_download for item in sublist]
