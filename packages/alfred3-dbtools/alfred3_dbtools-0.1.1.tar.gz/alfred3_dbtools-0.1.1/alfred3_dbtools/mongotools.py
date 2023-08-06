"""Tools for interacting with MongoDB databases."""

import copy

from pymongo import MongoClient
import alfred


class MongoDBConnector:
    """Connect to a MongoDB database or collection.
    
    :param str host: Hostname or IP address.
    :param int port: Port number on which to connect.
    :param str username: Username for authentication.
    :param str password: Password for authentication.
    :param str database: Database to which to the client will connect.
    :param str collection: Collection inside the specified database to which the client will connect. If left empty, the client will connect directly to the database.
    :param str auth_source: Database to authenticate on. Defaults to "admin", the MongoDB default.
    :param bool ssl: If ``True``, create a connection to the server using Transport Layer Security (TLS/SSL).
    :param str ca_file: Filepath to a file containing a single or a bundle of “certification authority” certificates, which are used to validate certificates passed from the other end of the connection. Implies ``tls=True``. Defaults to ``None``.
    """

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        database: str,
        collection: str=None,
        auth_source: str="admin",
        ssl: bool=False,
        ca_file: str=None,
    ):
        """Constructor method."""

        self._host = host
        self._port = port
        self._db_name = database
        self._collection = collection
        self._username = username
        self._password = password
        self._auth_source = auth_source
        self._ssl = ssl
        self._ca_file = ca_file

        self._client = None
        self._db = None

        self.connected = False

    def connect(self):
        """Establish the connection the MongoDB.

        If a collection was specified upon initialisation, the DBConnector will connect to this collection. Else, it will connect to the specified database.

        :return: The database or, if specified, collection given upon initialisation.
        """

        self._client = MongoClient(
            host=self._host,
            port=self._port,
            username=self._username,
            password=self._password,
            authSource=self._auth_source,
            tls=self._ssl,
            tlsCAFile=self._ca_file,
        )

        db = self._client[self._db_name]

        if self._collection:
            db = db[self._collection]

        self._db = db
        self.connected = True

        return self._db

    def disconnect(self):
        """Close the connection to the database."""

        self._client.close()
        self.connected = False

    @property
    def db(self):
        """Return the database or, if specified, collection given upon initialisation."""

        if self._db:
            return self._db
        else:
            return self.connect()


class ExpMongoDBConnector:
    """Connect to an alfred experiment's MongoDB collection.
    
    Connects to the same database and collection that the given alfred experiment uses to save its data. If multiple MongoSavingAgents are attached to the experiment, the ExpMongoDBConnector will connect to the MongoSavingAgent with the lowest activation level.

    :param experiment: An instance of ``alfred.Experiment``.
    :type experiment: class: `alfred.Experiment`
    :raise: ValueError if not initialised with an alfred experiment.
    """

    def __init__(self, experiment):
        """Constructor method."""

        self._exp = experiment
        self._agents = None
        
        self._client = None
        self._collection = None
        
        self.connected = False

        if not isinstance(self._exp, alfred.Experiment):
            raise ValueError("The input must be an instance of alfred.Experiment.")

    def _gather_agents(self):
        """Collect all MongoSavingAgents from the provided alfred experiment, sorted by activation level (lowest first)."""

        self._agents = []
        for agent in self._exp.saving_agent_controller._agents:
            if isinstance(agent, alfred.saving_agent.MongoSavingAgent):
                self._agents.append(copy.copy(agent))
        if not self._agents:
            raise ValueError("Your experiment needs at least one MongoSavingAgent for ExpMongoDBConnector to work.")
        self._agents.sort(key=lambda x: x.activation_level)
        
    def connect(self):
        """Establish a connection to the experiment's MongoDB with the lowest activation level.
        
        :return: The MongoClient collection from the MongoSavingAgent with lowest activation level.
        """        

        self._gather_agents()        
        
        if len(self._agents) > 1 and self._agents[0].activation_level == self._agents[1].activation_level:
            raise ValueError("There are two or more MongoSavingAgents with the highest activation level.")

        self._client = self._agents[0]._mc
        self._collection = self._agents[0]._col
        self.connected = True

        return self._collection
    
    def disconnect(self):
        """Close the connection to the database."""

        if self.connected:
            self._client.close()
            self.connected = False
    
    @property
    def db(self):
        """Return the experiment's MongoDB collection."""

        if self._collection:
            return self._collection
        else:
            return self.connect()
    
    @property
    def list_agents(self):
        """Return a list of all MongoSavingAgents belonging to the given alfred experiment."""
        if self._agents:
            return self._agents
        else:
            self._gather_agents()
            return self._agents
