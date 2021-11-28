"""
Provides functionality for creating the elasticsearch database
and fill it with random records
"""

from elasticsearch import Elasticsearch
import lorem
import names
import datetime
import random
import time
import logging

logger = logging.getLogger("db")

_DEFAULT_DOC_COUNT = 10
_DEFAULT_AUTHORS_COUNT = 10
_DEFAULT_DATETIME_START = datetime.date(2018, 1, 1)
_DEFAULT_DATETIME_END = datetime.datetime.date(datetime.datetime.now())
_DEFAULT_DATETIME_INTERVAL = (_DEFAULT_DATETIME_END - _DEFAULT_DATETIME_START).days
_DEFAULT_INDEX_NAME = "index-docs"
_DEFAULT_INDEX_PARS = "index-pars"


class ElasticSearchDocsGenerator():
    """
    class for generation of elasticsearch database and fill it with random records, that contains
    _DEFAULT_AUTHORS_COUNT different random authors, who all wrote together _DEFAULT_DOC_COUNT
    different random texts, at random time
    """
    def __init__(self, doc_count : int = _DEFAULT_DOC_COUNT,
                 authors_count : int = _DEFAULT_AUTHORS_COUNT,
                 index_name : str = _DEFAULT_INDEX_NAME,
                 datetime_interval : datetime.datetime = _DEFAULT_DATETIME_INTERVAL,
                 index_pars : str = _DEFAULT_INDEX_PARS,
                 datetime_start : datetime.datetime = _DEFAULT_DATETIME_START):
        """
        create the elasticsearch database and fill it with random records
        :param doc_count: number of documents
        :param authors_count: number of authors count
        :param index_name: name of index of authors records to fill to database
        :param datetime_interval: time interval (in days) when random text's was created
        :param index_pars: name of index of special parameters to fill to database
        :param datetime_start: start time of random text's generation
        :return: None
        """
        self.doc_count = doc_count
        self.authors_count = authors_count
        self.index_name = index_name
        self.index_pars = index_pars
        self.datetime_interval = datetime_interval
        self.datetime_start = datetime_start
        self.connect_elastic_net()
        self.fill_database_with_random_records()
        self.fill_database_with_pars()

    def connect_elastic_net(self):
        """
        Create elasticsearch database and clear it index_name and index_pars records.
        Elasticsearch tries to connect to 9200 port
        return None
        """
        self.es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
        logger.info("connected to Elasticsearch")
        self.es.indices.delete(index=self.index_name, ignore=[400, 404])
        self.es.indices.delete(index=self.index_pars, ignore=[400, 404])
        logger.debug("successfully connected to http://elasticsearch:9200")


    def get_elasticsearch_database(self) -> Elasticsearch:
        """
        Return the elasticsearch database with filled fields
        return: Elasticsearch database
        """
        self.es.indices.refresh(index=self.index_name)
        self.es.indices.refresh(index=self.index_pars)
        logger.info("return database")
        return self.es

    def generate_single_record(self) -> dict:
        """
        Generate single record, that contains random author name, random text and random date
        :return: record in dictionary form
        """
        #create random name
        random_author_id = random.randint(0, self.authors_count - 1)
        random_author = self.random_authors_list[random_author_id]
        #create random text paragraph
        random_text = lorem.paragraph()
        #create random datetime
        random_number_of_days = random.randrange(self.datetime_interval)
        random_day = self.datetime_start + datetime.timedelta(days=random_number_of_days)
        timetpl = random_day.timetuple()
        random_timestamp = time.mktime(timetpl)

        record = {
            "author" : random_author,
            "text" : random_text,
            "date": random_timestamp,
        }
        logger.debug("save author: %s, datetime: %s", random_author, random_day)
        return record

    def generate_pars_record(self, par_name : str, par_value : object) -> dict:
        """
        Generate record, that contains parameter name and parameter value
        :param par_name: name of the parameter
        :param par_value: value of the parameter
        :return: record in dictionary form
        """
        record = {
            "par" : par_name,
            "value" : par_value
        }
        return record

    def fill_database_with_pars(self):
        """
        Fill the database with important parameters
        :return: None
        """
        list_of_pars = [self.doc_count, self.authors_count, self.index_name]
        list_of_pars_names = ["doc_count", "authors_count", "index_name"]
        for ind, par in enumerate(list_of_pars):
            par_name = list_of_pars_names[ind]
            par_record = self.generate_pars_record(par_name, par)
            res = self.es.index(index=self.index_pars, id=ind + 1, document=par_record)
            logger.debug("set par: %s to database with value: %s", par_name, par)

    def fill_database_with_random_records(self):
        """
        Fill the database with random records
        :return: None
        """
        self.random_authors_list = [names.get_full_name() for _ in range(self.authors_count)]
        random_authors_list_record = self.generate_pars_record("authors_list", self.random_authors_list)
        res = self.es.index(index=self.index_pars, id=0, document=random_authors_list_record)
        logger.debug("generate random author names: %s", self.random_authors_list)

        for ind in range(self.doc_count):
            random_doc = self.generate_single_record()
            self.es.index(index=self.index_name, id=ind, document=random_doc)


def get_database() -> Elasticsearch:
    """
    Generate the elasticsearch database and fill it with random records
    :return: Elasticsearch database
    """
    es = ElasticSearchDocsGenerator()
    es_db = es.get_elasticsearch_database()
    return es_db

