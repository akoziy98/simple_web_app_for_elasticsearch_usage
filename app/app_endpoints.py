"""
Provides functionality for different endpoints
"""

from .db_controller import ElasticSearchController
import logging

logger = logging.getLogger("app_endpoints")


class TopAuthors():
    """
    Endpoint for obtaining top authors
    """
    def __init__(self, es_controller : ElasticSearchController):
        """
        Initialize class with elasticsearch database controller
        :param es_controller: controller of the elasticsearch database
        :return: None
        """
        self.es_controller = es_controller
        logger.debug("initialize TopAuthors endpoint")

    def get_n_top_authors(self, n : int) -> dict:
        """
        Return top n authors, ranked by number of written texts
        :param n: number of top authors. Important: this parameter should be less than
        total number of authors
        :return: dictionary of top authors in format: {"author_name" : number_of_texts}
        """
        logger.info("get top n: %s authors", n)
        dict_of_authors = self.es_controller.get_ranging_top_n_authors(n)
        logger.info("return dict of authors: %s", dict_of_authors)
        return dict_of_authors


class TextTimeCreation():
    """
    Endpoint for obtaining texts time creation distribution
    """
    def __init__(self, es_controller : ElasticSearchController):
        """
        Initialize class with elasticsearch database controller
        :param es_controller: controller of the elasticsearch database
        :return: None
        """
        self.es_controller = es_controller
        logger.debug("initialize TextTimeCreation endpoint")

    def get_datetime_documents_in_last_n_months(self, n : int) -> list:
        """
        Return ranked list of texts's creation time (in format "Y-m-d"), during last n moths
        :param n: number of last months
        :return: list of text's creation days in str format
        """
        logger.info("get datetime dustribution at last n: %s months", n)
        list_of_datetimes = self.es_controller.get_datetime_documents_in_last_n_months(n)
        logger.info("return list of datetimes: %s", list_of_datetimes)
        #convert datetimes to str format and flip it
        list_of_datetimes_str = [str(el) for el in list_of_datetimes[::-1]]
        return list_of_datetimes_str
