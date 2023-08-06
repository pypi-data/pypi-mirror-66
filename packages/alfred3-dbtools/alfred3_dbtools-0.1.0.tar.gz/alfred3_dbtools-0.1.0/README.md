# alfred3_dbtools

This module provides additional tools for working with databases in the context of alfred experiments (see [alfred on GitHub](https://github.com/ctreffe/alfred)).

## Installation

```bash
pip install alfred3_dbtools
```

## Usage

To import the tools for working with mongodb, include this statement at the beginning of your script:

```python
from alfred3_dbtools import mongotools
```

You can then access the classes provided in the module:

- `mongotools.MongoDBConnector` can be used to establish an independent connection to an instance of `pymongo.MongoClient`. Access to the client is provided via `mongotools.MongoDBConnector.db`. Depending on how the `MongoDBConnector` was initialised, this will return either a database instance or a specific collection inside a database.
    - Parameters: `host`, `port`, `username`, `password`, `database`, `collection` (defaults to `None`), `auth_source` (defaults to "admin"), `ssl` (defaults to `False`), `ca_file` (defaults to `None`). See `help(mongotools.MongoDBConnector)` for details.
- `mongotools.ExpMongoDBConnector` can be used to establish a connection to an experiments' MongoDBs.
    - The constructor takes one parameter: `experiment`, which needs to be an alfred experiment. See `help(mongotools.ExpMongoDBConnector)` for details.
    - `mongotools.ExpMongoDBConnector.db` will return the MongoDB collection of the `MongoSavingAgent` with the lowest activation level (i.e. the primary `MongoSavingAgent`). It will raise a `ValueError`, if the lowest activation level is occupied by two or more `MongoSavingAgent`s.
    - `mongotools.ExpMongoDBConnector.list_agents` will return a list of all `MongoSavingAgent`s added to the experiment.


Refer to the [pymongo documentation](https://pymongo.readthedocs.io/en/stable/tutorial.html) for further details on how to interact with the clients.

## Example of using `ExpMongoDBConnector`

``` Python
from alfred import Experiment
from alfred3_dbtools import mongotools

def generate_experiment(self, config=None):
    exp = Experiment(config=config)
    db_connector = mongotools.ExpMongoDBConnector(exp)
    db = db_connector.db

    first_exp = db.find_one({"exp_title": "Title goes here"})

    return exp
```

