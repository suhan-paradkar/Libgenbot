# -*- coding: utf-8 -*-
import pandas as pd
from difflib import SequenceMatcher

def similarStrings(a, b):
    return SequenceMatcher(None, a, b).ratio()

def filterJurnals(papers,csv_path):
    result = []
    df = pd.read_csv(csv_path, sep=";")
    journal_list = list(df["journal_list"])
    include_list = list(df["include_list"])

    for p in papers:
        good = False if (p.jurnal!=None and len(p.jurnal)>0) else True
        if p.jurnal!=None:
            for jurnal,include in zip(journal_list,include_list):
                if include==1 and similarStrings(p.jurnal,jurnal)>=0.8:
                    good = True

        if good == True:
            result.append(p)

    return result


def filter_min_date(list_papers,min_year):
    new_list = []

    for paper in list_papers:
        if paper.year!=None and int(paper.year)>=min_year:
             new_list.append(paper)

    return new_list

