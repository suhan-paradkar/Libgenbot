# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from .NetInfo import NetInfo
import requests

def schoolarParser(html):
    result = []
    soup = BeautifulSoup(html, "html.parser")
    for element in soup.findAll("div", class_="gs_r gs_or gs_scl"):
        if isBook(element) == False:
            title = None
            link = None
            link_pdf = None
            cites = None
            year = None
            authors = None
            for h3 in element.findAll("h3", class_="gs_rt"):
                found = False
                for a in h3.findAll("a"):
                    if found == False:
                        title = a.text
                        link = a.get("href")
                        found = True
            for a in element.findAll("a"):
                 if "Cited by" in a.text:
                     cites = int(a.text[8:])
                 if "[PDF]" in a.text:
                     link_pdf = a.get("href")
            for div in element.findAll("div", class_="gs_a"):
                try:
                    authors, source_and_year, source = div.text.replace('\u00A0', ' ').split(" - ")
                except ValueError:
                    continue

                if not authors.strip().endswith('\u2026'):

                    authors = authors.replace(', ', ';')
                else:
                    authors = None
                try:
                    year = int(source_and_year[-4:])
                except ValueError:
                    continue
                if not (1000 <= year <= 3000):
                    year = None
                else:
                    year = str(year)
            if title!=None:
                result.append({
                    'title' : title,
                    'link' : link,
                    'cites' : cites,
                    'link_pdf' : link_pdf,
                    'year' : year,
                    'authors' : authors})
    return result



def isBook(tag):
    result = False
    for span in tag.findAll("span", class_="gs_ct2"):
        if span.text=="[B]":
            result = True
    return result



def getSchiHubPDF(html):
    result = None
    soup = BeautifulSoup(html, "html.parser")

    iframe = soup.find(id='pdf')
    plugin = soup.find(id='plugin')

    if iframe!=None:
        result = iframe.get("src")

    if plugin!=None and result==None:
        result = plugin.get("src")

    if result!=None and result[0]!="h":
        result = "https:"+result

    return result

def getLibgenPDF(html):
    result = None
    soup = BeautifulSoup(html, "html.parser")

    iframe = soup.find(id='pdf')
    plugin = soup.find(id='plugin')

    if iframe!=None:
        result = iframe.get("src")

    if plugin!=None and result==None:
        result = plugin.get("src")

    if result!=None and result[0]!="h":
        result = "https:"+result

    return result


def SciHubUrls(html):
    result = []
    soup = BeautifulSoup(html, "html.parser")

    for ul in soup.findAll("ul"):
        for a in ul.findAll("a"):
            link = a.get("href")
            if link.startswith("https://sci-hub.") or link.startswith("http://sci-hub."):
                result.append(link)

    return result

def LibgenUrls(html):
    result = []
    soup = BeautifulSoup(html, "html.parser")

    for ul in soup.findAll("ul"):
        for a in ul.findAll("a"):
            link = a.get("href")
            if link.startswith("https://libgen.") or link.startswith("http://libgen."):
                result.append(link)

    return result

def bgcolorfx(tag):
    if tag.name == "tr":
        mbgcolor = tag.get("bgcolor", [])
        return "#C0C0C0" not in mbgcolor

def widthfx(tag):
    if tag.name == "td":
        width = tag.get("width", [])
        return "500" in width

def widthfox(tag):
    if tag.name == "td":
        width = tag.get("width", [])
        return "500" not in width

def linkparse(url):
    k = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'})
    kt = k.text
    soup = BeautifulSoup(kt, "html.parser")
    for element in soup.findAll("div", id="download"):
        for ul in element.findAll("ul"):
            for li in ul.findAll("li"):
                for a in li.findAll("a"):
                    if a.text == "IPFS.io":
                        link = a.get("href")

    if link != None:
        return link

def LibgenParser(html, genre):
    result = []
    if genre == 1:
        soup = BeautifulSoup(html, "html.parser")
        for element in soup.findAll("table", class_="c"):
            for tr in element.findAll(bgcolorfx):
                for td in tr.findAll(widthfx):
                    for a in tr.findAll("a"):
                        titlex = a.get("href")
                        if titlex.startswith("book/index"):
                            title = a.text
                        link = None
                        authors = None

                for td in tr.findAll(widthfox):
                    for a in td.findAll("a"):
                        if a.get("title") == None:
                            authors = a.text
                        if a.get("title") == "Gen.lib.rus.ec":
                            linkxf = a.get("href")
                            link = linkparse(linkxf)
                            result.append({
                                'title' : title,
                                'link' : link,
                                'authors' : authors})

    if genre == 2:
        soup = BeautifulSoup(html, "html.parser")
        for element in soup.findAll("table", class_="catalog"):
            for tbody in element.findAll("tbody"):
                for tr in tbody.findAll("tr"):
                    for td in tr.findAll("td"):
                        for ul in td.findAll("ul", class_="record_mirrors"):
                            for a in ul.findAll("a"):
                                if a.text =="Sci-Hub":
                                    link = a.get("href")
                        for p in td.findAll("p"):
                            for a in p.findAll("a"):
                                possible = a.get("href")
                                if possible.startswith("/scimag/journals"):
                                    jurnal = a.text
                                else:
                                    title = a.text

                        if not td.find("br"):
                            authors = td.text
                

                    if link!=None:
                        result.append({
                            'title' : title,
                            'link' : link,
                            'authors' : authors})
    if genre == 3:
        soup = BeautifulSoup(html, "html.parser")
        for element in soup.findAll("table", class_="catalog"):
            for tbody in element.findAll("tbody"):
                for tr in tbody.findAll("tr"):
                    title = None
                    for td in tr.findAll("td"):
                        for ul in tr.findAll("ul", class_="catalog_authors"):
                            for li in ul.findAll("li"):
                                for a in li.findAll("a"):
                                    authors = a.text
                        for a in td.findAll("a"):
                            fic = a.get("href")
                            if fic.startswith("fiction/"):
                                title = a.text
                        for ul in tr.findAll("ul", class_="record_mirrors_compact"):
                            for li in ul.findAll("li"):
                                for a in li.findAll("a"):
                                    if a.text == "[1]":
                                        linkx = a.get("href")
                                        link = linkparse(linkx)
                                        if title!=None:
                                            result.append({
                                                'title' : title,
                                                'link' : link,
                                                'authors' : authors})
    

    return result


def SciHubUrls(html):
    result = []
    soup = BeautifulSoup(html, "html.parser")

    for ul in soup.findAll("ul"):
        for a in ul.findAll("a"):
            link = a.get("href")
            if link.startswith("https://sci-hub.") or link.startswith("http://sci-hub."):
                result.append(link)

    return result


