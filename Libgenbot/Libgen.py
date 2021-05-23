import time
import requests
import functools
from .HTMLparsers import LibgenParser
from .Crossref import getPapersInfo
from .NetInfo import NetInfo

def libgen_requests(libgen_pages, url, restrict, libgen_results=25): 
    javascript_error = "Sorry, we can't verify that you're not a robot when JavaScript is turned off"
    
    to_download = []
    
    for i in libgen_pages:
        while True:
            res_url = url % (libgen_results * (i - 1))
            html = requests.get(res_url, headers=NetInfo.HEADERS)
            html = html.text

            if javascript_error in html:    
                is_continue = waithIPchange()
                
                if not is_continue:
                    return to_download
            
            else:
                break

        lpapers = libgenParser(html)
        print("\nLibgen page {} : {} papers found".format(i,libgen_results))

        if(len(lpapers)>0):
            papersInfo = getPapersInfo(lpapers, url, restrict, libgen_results)
            
            info_valids = functools.reduce(lambda a,b : a+1 if b.DOI!=None else a, papersInfo, 0)
            
            print("Papers found on Crossref: {}/{}\n".format(info_valids,len(lpapers)))

            to_download.append(papersInfo)
        
        else:
            print("Paper not found...")

    return to_download

def LibgenPapersInfo(lquery, libgen_pages, restrict, min_date=None, libgen_results=10):

    url = r"https://libgen.is/search.php?req="+lquery+"lg_topic=libgen&open=0&view=simple&res="+libgen_results+"&phrase=1&column=def"
    

    if len(lquery)>7 and (query[0:7]=="http://" or query[0:8]=="https://"):
         url = query

    to_download = libgen_requests(libgen_pages, url, restrict, libgen_results)

    return [item for sublist in to_download for item in sublist]
