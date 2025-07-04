import json
import logging

import requests
from bs4 import BeautifulSoup

from .helpers import normalize_paper_title
from .logger import logger
from .models import PaperData


def scrape_metadata(paper_data: PaperData) -> None:
    try:
        if paper_data.abs_url:
            if paper_data.src_website == "ArXiv":
                scrape_metadata_arxiv(paper_data)
            elif paper_data.src_website == "CVF":
                scrape_metadata_cvf(paper_data)
            elif paper_data.src_website == "ECVA":
                scrape_metadata_ecva(paper_data)
            elif paper_data.src_website == "NeurIPS":
                raise NotImplementedError("NeurIPS scraper is not implemented yet")
            elif paper_data.src_website == "OpenReview":
                raise NotImplementedError("OpenReview scraper is not implemented yet")
            else:
                # TODO: check here
                logger.error(f"Invalid source website: '{paper_data.src_website}'")
                return False
        else:
            # TODO: think how to handle this; maybe do nothing
            logger.warning("[Warn] No abstract URL")
    except Exception as err:
        logger.exception(err)
        logger.error("[Abort] Error while getting paper")
        return False


def scrape_metadata_arxiv(paper_data: PaperData) -> None:
    logger.setLevel(logging.DEBUG)
    logger.debug("[Processing] Retrieving paper metadata...")
    logger.setLevel(logging.WARNING)

    response = requests.get(paper_data.abs_url)
    if response.status_code != 200:
        logger.error(f"Cannot connect to {paper_data.abs_url}")
        raise Exception(f"Cannot connect to {paper_data.abs_url}")
    # make soup
    soup = BeautifulSoup(response.text, "html.parser")

    # get TITLE
    result = soup.find("h1", class_="title mathjax")
    tmp = [i.string for i in result]
    paper_title = tmp.pop()
    paper_data.title = paper_title

    # get AUTHORS
    result = soup.find("div", class_="authors")

    try:
        author_list = [i.string.strip() for i in result if i.string]
        author_list.pop(0)
        while "," in author_list:
            author_list.remove(",")
        paper_data.authors = author_list
    except AttributeError:
        paper_data.authors = []
        logger.warning("[Warn] Unable to retrieve long author list")

    # get ABSTRACT
    result = soup.find("blockquote", class_="abstract mathjax")
    tmp = [i.string for i in result]
    paper_abstract = tmp.pop()
    tmp = paper_abstract.split("\n")
    paper_abstract = " ".join(tmp)
    paper_data.abstract = paper_abstract.strip()

    # get COMMENTS
    result = soup.find("td", class_="tablecell comments mathjax")
    if result:
        comments = [i.string.strip() if i.string else "" for i in result]
        comments = " ".join(comments)
    else:
        comments = ""
    paper_data.comments = comments.strip()

    # get PWC (paper with code)
    # API: https://arxiv.paperswithcode.com/api/v0/papers/{paper_id}
    pwc_url = f"https://arxiv.paperswithcode.com/api/v0/papers/{paper_data.paper_id}"
    pwc_response = requests.get(pwc_url)
    if pwc_response.status_code == 200:
        pwc = pwc_response.text
        pwc = json.loads(pwc)
        official_code_urls: list = pwc.get("all_official", [])
        official_code_urls: list = [i.get("url") for i in official_code_urls]
        pwc_page_url: str = pwc.get("paper_url", "")
    else:
        official_code_urls = []
        pwc_page_url = ""
    paper_data.official_code_urls = official_code_urls
    paper_data.pwc_page_url = pwc_page_url.strip()

    # get BIBTEX
    bibtex_url = f"https://arxiv.org/bibtex/{paper_data.paper_id}"
    bibtex_response = requests.get(bibtex_url)
    if bibtex_response.status_code == 200:
        bibtex = bibtex_response.text
    else:
        bibtex = ""
    paper_data.bibtex = bibtex.strip()

    # construct filename
    paper_data.download_name = (
        f"{paper_data.paper_id}_{normalize_paper_title(paper_data.title)}.pdf"
    )

    return None


def scrape_metadata_cvf(paper_data: PaperData) -> None:
    logger.setLevel(logging.DEBUG)
    logger.debug("[Processing] Retrieving paper metadata from CVF...")
    logger.setLevel(logging.WARNING)

    response = requests.get(paper_data.abs_url)
    if response.status_code != 200:
        logger.error(f"Cannot connect to {paper_data.abs_url}")
        raise Exception(f"Cannot connect to {paper_data.abs_url}")
    # make soup
    soup = BeautifulSoup(response.text, "html.parser")

    # get TITLE
    result = soup.find("div", id="papertitle")
    tmp = [i.string.strip() for i in result if i.string]
    paper_title = tmp[0].strip()  # NOTE: hardcoded
    paper_data.title = paper_title
    # print(paper_title)

    # get AUTHORS
    result = soup.find("div", id="authors")
    tmp = [i.string.strip() for i in result if i.string]
    authors_str = tmp[1].strip()  # NOTE: hardcoded
    authors_list = [x.strip() for x in authors_str.split(",") if x]
    paper_data.authors = authors_list
    # print(authors_list)

    # get ABSTRACT
    result = soup.find("div", id="abstract")
    tmp = [i.string.strip() for i in result if i.string]
    paper_abstract = "".join(tmp)
    paper_data.abstract = paper_abstract.strip()
    # print(paper_abstract)

    # get BIBTEX
    result = soup.find("div", class_="bibref")
    tmp = [i.string.strip() for i in result if i.string]
    bibtex = "".join(tmp)
    paper_data.bibtex = bibtex.strip()
    # print(bibtex)

    # NOTE: this doesn't work cuz it's a relative path and the path construction is different every year
    # get pdf link
    # result = soup.find_all("a", string="pdf")
    # if len(result) == 1:
    #     pdf_url = result[0].get("href")
    #     paper_data.pdf_url = f"https://openaccess.thecvf.com{pdf_url.strip()}"

    # get supplementary path
    result = soup.find_all("a", string="supp")
    if len(result) == 1:
        supp_url = result[0].get("href")
        paper_data.supp_url = f"{supp_url.strip()}"

    return None


def scrape_metadata_ecva(paper_data: PaperData) -> None:
    # TODO
    logger.setLevel(logging.DEBUG)
    logger.debug("[Processing] Retrieving paper metadata...")
    logger.setLevel(logging.WARNING)

    response = requests.get(paper_data.abs_url)
    if response.status_code != 200:
        logger.error(f"Cannot connect to {paper_data.abs_url}")
        raise Exception(f"Cannot connect to {paper_data.abs_url}")
    # make soup
    soup = BeautifulSoup(response.text, "html.parser")

    # get TITLE
    result = soup.find("div", id="papertitle")
    tmp = [i.string.strip() for i in result if i.string]
    paper_title = tmp[0].strip()  # NOTE: hardcoded
    paper_data.title = paper_title
    # print(paper_title)

    # get AUTHORS
    result = soup.find("div", id="authors")
    tmp = [i.string.strip() for i in result if i.string]
    authors_str = tmp[0].strip()  # NOTE: hardcoded
    authors_list = [x.strip(" *") for x in authors_str.split(",") if x]
    paper_data.authors = authors_list
    # print(authors_list)

    # get ABSTRACT
    result = soup.find("div", id="abstract")
    tmp = [i.string.strip() for i in result if i.string]
    paper_abstract = "".join(tmp)
    paper_data.abstract = paper_abstract.strip(' "')
    # print(paper_abstract)

    # get pdf path
    result = soup.find_all("a", string="pdf")
    if len(result) == 1:
        pdf_url = result[0].get("href")
        if pdf_url.startswith("../../../../"):
            pdf_url = pdf_url.replace("../../../../", "https://www.ecva.net/")
            paper_data.pdf_url = pdf_url
        else:
            # TODO: check here
            # print("Unexpected pdf_url:", pdf_url)
            pass

    # get doi url
    result = soup.find_all("a", string="DOI")
    if len(result) == 1:
        doi_url = result[0].get("href")
        if doi_url.startswith("https"):
            paper_data.doi_url = doi_url
        else:
            # TODO: check here
            # print("Unexpected doi_url:", doi_url)
            pass

    # get supplementary path
    result = soup.find_all("a", string="supplementary material")
    if len(result) == 1:
        supp_url = result[0].get("href")
        if supp_url.startswith("../../../../"):
            supp_url = supp_url.replace("../../../../", "https://www.ecva.net/")
            paper_data.supp_url = supp_url
        else:
            # TODO: check here
            # print("Unexpected supp_url:", supp_url)
            pass

    # construct filename
    paper_data.download_name = f"{paper_data.year}_{paper_data.paper_venue}_{paper_data.paper_id}_{normalize_paper_title(paper_data.title)}.pdf"

    return None


def scrape_metadata_nips(paper_data: PaperData) -> None:
    # TODO
    ...


def scrape_metadata_openreview(paper_data: PaperData) -> None:
    # TODO
    ...


if __name__ == "__main__":
    ...
