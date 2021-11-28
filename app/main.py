"""
Main file for starting web application
Consists of database creation. Due to it's a learning task, we define database
creation here.
Also consists of FastApi initializing and defining of all possible queries
"""

from fastapi import FastAPI
import logging

from .setup_logging import setup_logging
from .db import *
from .db_controller import *
from .app_endpoints import *

_DEFAULT_LOGGER_CONFIG_FILEPATH = "app/loger_config/main_log.conf.yml"

setup_logging(_DEFAULT_LOGGER_CONFIG_FILEPATH)
logger = logging.getLogger("main_app")

#create the database
es_db = get_database()
es_controller = ElasticSearchController(es_db)

#create the endpoints classes
top_authors = TopAuthors(es_controller)
text_time_creation = TextTimeCreation(es_controller)

#initialize api
app = FastAPI()

@app.get("/")
def home() -> dict:
    """
    Return a welcome message
    :return: welcome message in dict fromat: {"message" : "message_text"}
    """
    return {"message" : "Welcome to simple Web application by Andrey Koziy"}


@app.get("/documents/authors/top/{n}/", tags=["documents"])
def get_n_top_authors(n : int) -> dict:
    """
    Return top n authors dictionary, ranked by number of texts
    param n: number of top authors. Important: this parameter should be less than
    total number of authors
    :return: dictionary of top authors in format: {"author_name" : number_of_texts}
    """
    res_top_authors = top_authors.get_n_top_authors(n)
    logger.info("top n: %s authors is: %s", n, res_top_authors)
    return res_top_authors


@app.get("/documents/dates/lastmonths/{n}/", tags=["documents"])
def get_datetime_documents_in_last_n_months(n : int) -> list:
    """
    Return ranked list of texts's creation time (in format "Y-m-d"), during last n moths
    :param n: number of last months
    :return: list of text's creation days in str format
    """
    res_datetime_documents = text_time_creation.get_datetime_documents_in_last_n_months(n)
    logger.info("datetime distribution at last n: %s months: %s", n, res_datetime_documents)
    return res_datetime_documents
