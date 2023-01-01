# -*- coding: utf-8 -*-

# GLOBAL IMPORTS
import sys
import abc
import collections
from multiprocessing.sharedctypes import Value
from sys import argv
from requests.exceptions import ConnectionError
import pymongo
from pymongo import MongoClient
sys.path.insert(0, "C:\\Users\\dario\\pet_projects\\tmts-oracle-app")
from utils.utils import *

class MongoDbInterface(metaclass=abc.ABCMeta):
    """ Abstract API to database. Provides basic abstract method for connection to a host.

    Args:
        metaclass (_type_, optional): _description_. Defaults to abc.ABCMeta.

    Raises:
        NotImplementedError: _description_
        NotImplementedError: _description_
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, '_set_host') and 
                callable(subclass._set_host) and 
                hasattr(subclass, '_set_database') and 
                callable(subclass._set_database) or 
                NotImplemented)

    def __init__(self, host_url: str, database_name: str) -> None:
        """Constructor of metaclass database interface for MongoDb.

        Args:
            host_url (str): url for host location.
            database_name (str): database name.
        """
        if not isinstance(host_url, str):
            raise TypeError("Host url must be an instance of str")
        if not isinstance(database_name, str):
            raise TypeError("Host url must be an instance of str")
        self._host = self._set_host(host_url)
        # TODO: version validation condition.
        self._version = self._host.server_info()['version']
        self._db_collections = []
        self._db = self._set_database(database_name)

    @classmethod
    def get_databases_in_any_host(self, host: str) -> list:
        """ A general method that returns all databases for any host instance.

        Args:
            host (str): _description_

        Returns:
            list: _description_
        """
        pass

    @classmethod
    def get_collections_in_any_database(self, host:str, database: str) -> list:
        """A general method that returns the collections for any database in any host instance.

        Args:
            host (str): _description_
            database (str): _description_

        Returns:
            list: _description_
        """
        pass

    def _set_host(self, str) -> object:
        """_summary_

        Args:
            str (_type_): URL string for initiating connection to host.

        Returns:
            object: Pymongo MongoCliente class instance.
        """
        try:
            host = MongoClient(str)
        except ConnectionError as e:
            print(['EXCEPTION'], e)
        return host
    
    def _set_database(self, str) -> object:
        """_summary_

        Args:
            str (_type_): database name.

        Returns:
            object: Pymongo database class instance.
        """
        if str not in self._host.list_database_names():
            raise Exception("Database provided does not exist in host: {}. Please enter one of the available databases: [{}]".format(self._host.HOST, self._host.list_databases_names()))
        else:
            try:
                db = self._host[str]
                self._db_collections.extend(self._read_database_collections(db))
            except ValueError as e:
                print(['Input an existing database name'], e)
            return db

    def _read_database_collections(self, obj) -> list:
        """ Return a list of strings containing all collections in a database

        Args:
            obj (_type_): Pymongo database class instance

        Returns:
            list: list of strings with names of all database collections.
        """
        db_collections = obj.list_collection_names()
        return db_collections

    @property
    def collections(self) -> list:
        """Getter method for collection attribute.

        Returns:
            list: list of string names corresponding to each available collection.
        """
        if len(self._db_collections) < 1:
            raise Exception('There are no collection for the current database')
        else:
            return self._db_collections



class CompanyDbInterface(MongoDbInterface):
    """Subclass of MongoDbInterface. Adds read-only operations.

    Args:
        MongoDbInterface (_type_): _description_
    """
    # Global flags for activating descriptor fucntionality in @Mutable decorator. Subclasses do not have access to get_database_in_any_host() and get_collections_in_any_database() methods.
    databases = True
    databaseCollections = True

    def __init__(self, host_url = "mongodb://localhost:27017", database_name = "admin"):     
        super().__init__(host_url, database_name)

    def _get_single_collection(self, str) -> object:
        
        """ A method that returns a pymongo.collection.collection object in case the pass argument exists in self.

        Args:
            str (_type_): Collection name.

        Returns:
            object: Pymongo collection class instance.
        """
        if str not in self._db_collections:
            raise Exception("Collection provided does not exist in database {}. Please enter one of the available collections: {}".format(self._db.name, self._db.list_collection_names()))
        else:
            try:
                collection = self._db[str]
            except ValueError as e:
                print(['EXCEPTION'], e)
        return collection

    def find_values_for_one_key(self, collection: str, key: str) -> object:
        """ Method that finds values for single key and returns a cursor object with search result in database.

        Args:
            key (str): key/field to search in database.

        Returns:
            object: A pymongo.cluster.Cursor object with packed data.
        """
        collection = self._get_single_collection(collection)
        return collection.find({}, {key})

    def _find_values_for_multiple_keys(self, collection: str, keys: list) -> object:
        """ Method that finds values for multiple input keys and returns a cursor object with search result in database.

        Args:
            key (str): key/field to search in database.

        Returns:
            object: A pymongo.cluster.Cursor object with packed data.
        """
        collection = self._get_single_collection(collection)
        return collection.find({}, set(keys))

