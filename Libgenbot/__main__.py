# -*- coding: utf-8 -*-

import argparse
import sys
from .Paper import Paper
from .PapersFilters import filterJurnals, filter_min_date, similarStrings
from .Downloader import downloadPapers
from .Downloader import downloadlibgenPapers
from .Scholar import ScholarPapersInfo
from .Crossref import getPapersInfoFromDOIs
from .proxy import proxy
from .Libgen import LibgenPapersInfo

def scholar_start(scholar_query, scholar_results, scholar_pages, dwn_dir, proxy, min_date=None, num_limit=None, num_limit_type=None, filter_jurnal_file=None, restrict=None, DOIs=None, SciHub_URL=None):

    to_download = []
    if DOIs==None:
        print("Scholar Query: {}".format(scholar_query))
        to_download = ScholarPapersInfo(scholar_query, scholar_pages, restrict, min_date, scholar_results)
    else:
        print("Downloading papers from DOIs\n")
        num = 1
        i = 0
        while i<len(DOIs):
            DOI = DOIs[i]
            print("Searching paper {} of {} with DOI {}".format(num,len(DOIs),DOI))
            papersInfo = getPapersInfoFromDOIs(DOI, restrict)
            to_download.append(papersInfo)

            num += 1
            i +=  1


    if restrict!=0 and to_download:
        if filter_jurnal_file!=None:
           to_download = filterJurnals(to_download,filter_jurnal_file)

        if min_date!=None:
            to_download = filter_min_date(to_download,min_date)

        if num_limit_type!=None and num_limit_type==0:
            to_download.sort(key=lambda x: int(x.sc_year) if x.sc_year!=None else 0, reverse=True)

        if num_limit_type!=None and num_limit_type==1:
            to_download.sort(key=lambda x: int(x.sc_cites) if x.sc_cites!=None else 0, reverse=True)

        downloadPapers(to_download, dwn_dir, num_limit, SciHub_URL)


    Paper.generateReport(to_download,dwn_dir+"result.csv")
    Paper.generateBibtex(to_download,dwn_dir+"bibtex.bib")


def start(query, results, pages, genre, dwn_dir, proxy, num_limit=None, num_limit_type=None, filter_jurnal_file=None, restrict=None, DOIs=None, Libgen_URL=None):

    to_download = []
    print("Query: {}".format(query))
    to_download = LibgenPapersInfo(query, pages, genre, restrict, results)

    downloadlibgenPapers(to_download, dwn_dir, num_limit, results)


    Paper.generateReport(to_download,dwn_dir+"result.csv")
    Paper.generateBibtex(to_download,dwn_dir+"bibtex.bib")


def main():
    print("""Libgenbot is a simple bot written in python inspired by PyPaperBot""")

    parser = argparse.ArgumentParser(description='Libgenbot is python tool to search and download any article using Libgen')
    
    parser.add_argument('--query', '-q', type=str, default=None, help='Query to make on Libgen')
    
    parser.add_argument('--scholar-query', '-sq', type=str, default=None, help='query to be made on Google Scholar')
    
    parser.add_argument('--doi', type=str, default=None, help='DOI of the paper to download (this option uses only Libgen to download)')
    
    parser.add_argument('--doi-file', type=str, default=None, help='File .txt containing the list of paper\'s DOIs to download')
    
    parser.add_argument('--scholar-pages', '-sp', type=str, help='If given in %%d format, the number of pages to download from the beginning. '
                                                               'If given in %%d-%%d format, the range of pages (starting from 1) to download (the end is included). '
                                                               'Each page has a maximum of 10 papers (required for --scholar-query')
    
    parser.add_argument('--libgen-pages', '-p', type=str, help='If given in %%d format, the number of pages to download'
                                                              'If given in %%d-%%d format, the range of pages (starting from 1) to download'
                                                              'Each page has a maximum of 100 papers (required for --query)')
    
    parser.add_argument('--dwn-dir', type=str, help='Directory path in which to save the results')
    
    parser.add_argument('--min-year', default=None, type=int, help='Minimal publication year of the paper to download')
    
    parser.add_argument('--max-dwn-year', default=None, type=int, help='Maximum number of papers to download sorted by year')
    
    parser.add_argument('--max-dwn-cites', default=None, type=int, help='Maximum number of papers to download sorted by number of citations')
    
    parser.add_argument('--journal-filter', default=None, type=str ,help='CSV file path of the journal filter (More info on github)')
    
    parser.add_argument('--restrict', default=None, type=int ,choices=[0,1], help='0:Download only Bibtex - 1:Down load only papers PDF')
    
    parser.add_argument('--scihub-mirror', default=None, type=str, help='Mirror for downloading papers from sci-hub. If not set, it is selected automatically')

    parser.add_argument('--libgen-mirror', default=None, type=str, help='Mirror for downloading papers from Libgen. If not set, it is selected automatically')

    parser.add_argument('--scholar-results', default=10, type=int, choices=[1,2,3,4,5,6,7,8,9,10], help='Downloads the first x results in a scholar page(max=10)')
    
    parser.add_argument('--libgen-results', default=10, type=int, help='Downloads the first x result of a Libgen page(max=100)')
    
    parser.add_argument('--proxy', nargs='*', default=[], help='Use proxychains, provide comma seperated list of proxies to use and please, no spaces' 
                                                                'Feature currently in alpha and may contain bugs')
    
    parser.add_argument('--genre', default=None, type=int, choices=[1,2,3,4,5,6], help='select genre: one of' 
                    'libgen(Sci-Tech)[1]'
                    'Scientific articles[2]'
                    'Fiction[3]')

    args = parser.parse_args()

    pchain = []
    pchain = args.proxy

    proxy(pchain)

    if (args.query!=None and args.genre==None):
        print("Error, no genre selected")
        sys.exit()

    if (args.query!=None and args.doi_file!=None) or (args.query!=None and args.doi!=None) or (args.doi!=None and args.doi_file!=None) or (args.scholar_query!=None and args.doi.file!=None) or (args.scholar_query!=None and args.doi!=None) or (args.query!=None and args.scholar_query!=None):
        print("Error: Only one option between '--query', '--scholar-query', '--doi-file' and '--doi' can be used")
        sys.exit()

    if args.dwn_dir==None:
        print("Error, provide the directory path in which to save the results")
        sys.exit()

    if (args.libgen_results >= 100) or (args.libgen_results <= 0):
        print("Error: value of --libgen-results must be between 0 to 100")
        sys.exit()

    if (args.scholar_results!=10 and args.scholar_pages!=1):
        print("Scholar results best applied along with --scholar-pages=1")

    dwn_dir = args.dwn_dir.replace('\\', '/')
    if dwn_dir[len(dwn_dir)-1]!='/':
        dwn_dir = dwn_dir + "/"

    if args.max_dwn_year != None and args.max_dwn_cites != None:
        print("Error: Only one option between '--max-dwn-year' and '--max-dwn-cites' can be used ")
        sys.exit()

    if(args.query != None):
        if args.libgen_pages:
            try:
                split = args.libgen_pages.split('-')
                if len(split) == 1:
                    libgen_pages = range(1, int(split[0]) + 1)
                elif len(split) == 2:
                    start_page, end_page = [int(x) for x in split]
                    libgen_pages = range(start_page, end_page + 1)
                else:
                    raise ValueError
            except Exception:
                print(r"Error: Invalid format for --libgen-pages option. Expected: %d or %d-%d, got: " + args.libgen_pages)
                sys.exit()
        else:
            print("Error: with --libgen-query provide also --libgen-pages")
            sys.exit()
    else:
        libgen_pages = 0


    if(args.scholar_query != None):
        if args.scholar_pages:
            try:
                split = args.scholar_pages.split('-')
                if len(split) == 1:
                    scholar_pages = range(1, int(split[0]) + 1)
                elif len(split) == 2:
                    start_page, end_page = [int(x) for x in split]
                    scholar_pages = range(start_page, end_page + 1)
                else:
                    raise ValueError
            except Exception:
                print(r"Error: Invalid format for --scholar-pages option. Expected: %d or %d-%d, got: " + args.scholar_pages)
                sys.exit()
        else:
            print("Error: with --scholar-query provide also --scholar-pages")
            sys.exit()
    else:
        scholar_pages = 0


    DOIs = None
    if args.doi_file != None:
        DOIs = []
        f = args.doi_file.replace('\\', '/')
        with open(f) as file_in:
            for line in file_in:
                if line[len(line)-1]=='\n':
                    DOIs.append(line[:-1])
                else:
                    DOIs.append(line)

    if args.doi!=None:
        DOIs = [args.doi]

    max_dwn = None
    max_dwn_type = None
    if args.max_dwn_year != None:
        max_dwn = args.max_dwn_year
        max_dwn_type = 0
    if args.max_dwn_cites != None:
        max_dwn = args.max_dwn_cites
        max_dwn_type = 1

    if args.query != None:
        start(args.query, args.libgen_results, args.libgen_pages, args.genre, dwn_dir, proxy, max_dwn, max_dwn_type , args.journal_filter, args.restrict, DOIs, args.libgen_mirror)

    if (args.scholar_query != None) or (args.doi != None):
         scholar_start(args.scholar_query, args.scholar_results, args.scholar_pages, dwn_dir, proxy, args.min_year , max_dwn, max_dwn_type , args.journal_filter, args.restrict, DOIs, args.libgen_mirror)


if __name__ == "__main__":
    main()
