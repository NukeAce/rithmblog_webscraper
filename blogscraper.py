"""Blogscraper: This script creates a csv file from https://www.rithmschool.com/blog
containing blog title,time and url.
"""
import csv
from time import sleep

import requests
from bs4 import BeautifulSoup


def article_write(soup_obj, csv_writer_obj):
    """Writes the title, time and url from https://www.rithmschool.com/blog
    into a csv file.
    Parameters
    ----------

    soup_obj: object
        `Beautiful Soup` object.

    csv_writer_obj: object
        `csv.writer` object.
    """
    articles_ = soup_obj.findAll("article")
    for article in articles_:
        a_tag_ = article.find("a")
        title = a_tag_.get_text()
        url = a_tag_["href"]
        time_tag = article.find("time")
        time = time_tag["datetime"]
        csv_writer_obj.writerow(
            [title, time, f'https://www.rithmschool.com{url}'])


response = requests.get("https://www.rithmschool.com/blog")
soup = BeautifulSoup(response.text, "html.parser")
spans = soup.find_all("span", attrs={"class": "page"})
articles = soup.findAll("article")
with open("articles.csv", "w") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(["Title", "Time", "Url"])
    for span in spans:
        a_tag = span.find("a")
        if a_tag is not None:
            url_complete = a_tag["href"]
            sleep(3)
            response = requests.get(
                f"https://www.rithmschool.com{url_complete}")
            soup = BeautifulSoup(response.text, "html.parser")
            article_write(soup, csv_writer)
        else:
            article_write(soup, csv_writer)
