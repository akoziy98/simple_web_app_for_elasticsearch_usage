"""
Controller of database provides functionality for
elasticsearch database management
"""

import datetime
import time
import logging
from elasticsearch import Elasticsearch

logger = logging.getLogger("db_controller")

_DEFAULT_INDEX_PARS = "index-pars"


class ElasticSearchController():
    """
    Class for management of elasticsearch database
    """
    def __init__(self, es : Elasticsearch, index_par : str = _DEFAULT_INDEX_PARS):
        """
        Initialize controller for elasticsearch database, that was filled in special format,
        with index of parameters records index_par
        :param es: Elasticsearch database
        :param index_par: index of parameters records in database
        :return: None
        """
        self.es = es
        self.index_pars = index_par
        self.doc_count = self.get_par_by_name("doc_count")
        self.authors_count = self.get_par_by_name("authors_count")
        self.index_name = self.get_par_by_name("index_name")
        self.authors_list = self.get_par_by_name("authors_list")

    def get_par_by_name(self, name : str) -> object:
        """
        Return parameter in databse by it's name
        :param name: name of the parameter
        :return: value of the parameter, that can be int or str
        """
        res = self.es.search(index=self.index_pars, query={"match": {"par": name}})
        res = res["hits"]["hits"][0]["_source"]["value"]
        logger.debug("get parameter with name: %s and value: %s", name, res)
        return res

    def get_ranging_top_n_authors(self, n : int) -> dict:
        """
        Return top n authors, that ranked by number of texts
        :param n: number of top authors need to be returned.
        Important: this parameter should be less than total number of authors
        :return: dictionary of top authors in format: {"author_name" : number_of_texts}
        """
        count_of_authors = len(self.authors_list)
        if n <= count_of_authors:
            count_list_sorted = self.ranging_all_authors()
            logger.debug("count list sorted: %s", count_list_sorted)
            return dict(count_list_sorted[:n])
        else:
            msg = ("n parameter should be lower or equal, than authors count. " \
                  "Current n: %s; Authors count: %s", n, count_of_authors)
            logger.warning(msg)
            raise ValueError(msg)

    def ranging_all_authors(self) -> list:
        """
        Sorting all authors by their number of texts
        :return: list of tuples, each one has the next form: ("author_name", number_of_texts)
        """
        count_dict = self.get_authors_text_count_dict()
        count_list_sorted = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
        return count_list_sorted

    def get_authors_text_count_dict(self) -> dict:
        """
        Return unsorted dictionary of different authors and number of their texts
        :return: dictionary of authors in format: {"author_name" : number_of_texts}
        """
        count_dict = {}
        for name in self.authors_list:
            count_text = self.get_count_text_by_author(name)
            count_dict[name] = count_text
        logger.debug("authors text count dict: %s", count_dict)
        return count_dict

    def get_count_text_by_author(self, name : str) -> int:
        """
        Return number of texts of specific author with "name"
        :param name: name of specific author
        :return: number of author's texts
        """
        res = self.es.search(index=self.index_name, query={"match": {"author": name}})
        count_text = res["hits"]["total"]["value"]
        return count_text

    def get_datetime_documents_in_last_n_months(self, n : int) -> list:
        """
        Return sorted array of texts datetimes, which was written at last n months
        :param n: number of last n moths
        :return: list of sorted datetimes
        """
        date_now = datetime.datetime.date(datetime.datetime.now())
        year_prev = date_now.year - n // 12
        month_prev = date_now.month - n % 12
        date_prev = date_now.replace(month=month_prev, year=year_prev)
        # convert dates to timestamp
        timetpl = date_prev.timetuple()
        timestamp_prev = time.mktime(timetpl)

        res = self.get_documents_in_last_n_months(timestamp_prev)
        count_of_documents = res["hits"]["total"]["value"]
        list_of_datetimes = []
        if count_of_documents > 0:
            for ind in range(count_of_documents):
                current_timestamp = res["hits"]["hits"][ind]["_source"]["date"]
                current_date = datetime.datetime.fromtimestamp(current_timestamp)
                current_date = datetime.datetime.date(current_date)
                list_of_datetimes.append(current_date)
        return sorted(list_of_datetimes)

    def get_documents_in_last_n_months(self, timestamp_prev : float) -> dict:
        """
        Return result of search in elasticsearch database for all texts,
        that was written after the timestamp_prev
        :param timestamp_prev: the lower timestamp boundary to obtain texts
        :return: dictionary, that represents search result in elasticsearch database
        """
        query = {'range': {'date': {'gte': timestamp_prev}}}
        res = self.es.search(index=self.index_name, query=query)
        return res
