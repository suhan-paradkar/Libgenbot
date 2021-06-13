# -*- coding: utf-8 -*-
import bibtexparser
import re
import csv
import os

class lPaper:


    def __init__(self,title=None, libgen_link=None, libgen_page=None, authors=None):
        self.title = title
        self.libgen_page = libgen_page
        self.libgen_link = libgen_link
        self.authors = authors

        self.jurnal = None
        self.cites_num = None
        self.bibtex = None

        self.downloaded = False
        self.downloadedFrom = "Libgen"



    def getFileName(self):
        try:
            return re.sub('[^\w\-_\. ]', '_', self.title)+".pdf"
        except:
            return "none.pdf"

    def setBibtex(self,bibtex):
        x=bibtexparser.loads(bibtex, parser=None)
        x=x.entries

        self.bibtex = bibtex

        try:
            if 'author' in x[0]:
                self.authors = x[0]["author"]
            self.jurnal=x[0]["journal"].replace("\\","") if "journal" in x[0] else None
            if self.jurnal==None:
                 self.jurnal=x[0]["publisher"].replace("\\","") if "publisher" in x[0] else None

        except:
            pass




    def generateReport(papers, path):
        with open(path, mode="w", encoding='utf-8', newline='', buffering=1) as w_file:
            content = ["Name", "Libgen Link", "DOI", "Bibtex",
                       "PDF Name", "Libgen page", "Journal",
                       "Downloaded", "Authors"]
            file_writer = csv.DictWriter(w_file, delimiter = ",", lineterminator=os.linesep, fieldnames=content)
            file_writer.writeheader()

            for p in papers:
                pdf_name = p.getFileName()
                bibtex_found = True if p.bibtex!=None else False

                file_writer.writerow({
                        "Name" : p.title,
                        "Libgen Link" : p.libgen_link,
                        "DOI" : p.DOI,
                        "Bibtex" : bibtex_found,
                        "PDF Name" : pdf_name,
                        "Libgen page" : p.libgen_page,
                        "Journal" : p.jurnal,
                        "Downloaded" : p.downloaded,
                        "Authors" : p.authors})


    def generateBibtex(papers, path):
        content = ""
        for p in papers:
            if p.bibtex!=None:
                content += p.bibtex+"\n"


        relace_list = ["\ast","*","#"]
        for c in relace_list:
            content = content.replace(c,"")

        f = open(path, "w", encoding="latin-1", errors="ignore")
        f.write(str(content))
        f.close()
