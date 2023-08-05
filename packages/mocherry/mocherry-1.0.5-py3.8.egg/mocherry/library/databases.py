#!/usr/bin/env python
from mongoengine import connect

class DatabaseConnection:
    def __init__(self, uri, alias=None):
        self.uri = uri
        self.alias = "default" if alias is None else alias

    def __enter__(self):
        self.conn = connect(host=self.uri, alias=self.alias, minPoolSize=10, maxPoolSize=250)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        pass
