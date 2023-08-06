import itertools

import pycountry
from pycountry.db import Database as Base, logger

pycountry.countries._load()


class Database(Base):
    def __init__(self, name, keys):
        self.data_class_name = name
        self.keys = keys
        super().__init__(None)

    def _load(self):
        if self._is_loaded:
            return

        self.objects = []
        self.index_names = set()
        self.indices = {}
        self.data_class = Country
        lst = [pycountry.countries.get(alpha_3=key)._fields for key in self.keys]

        for entry in lst:
            obj = self.data_class(**entry)
            self.objects.append(obj)

            # Inject into index.
            for key, value in entry.items():
                if key in self.no_index:
                    continue
                index = self.indices.setdefault(key, {})
                if value in index:
                    logger.debug(
                        "%s %r already taken in index %r and will be "
                        "ignored. This is an error in the databases."
                        % (self.data_class_name, value, key)
                    )
                index[value] = obj

        self._is_loaded = True


class Country(pycountry.countries.data_class):
    _fields: dict

    def __eq__(self, other):
        if isinstance(other, pycountry.countries.data_class):
            return self._fields == other._fields
        return NotImplemented


def aggregate(name: str, *args: Database):
    """
    Aggregate all keys from the given sequence of databases into a single
    database with the given name.
    """
    keys = set(itertools.chain(*(db.keys for db in args)))
    return Database(name, keys)
