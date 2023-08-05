#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 08:03:58 2020

@author: Rajiv Sambasivan
"""

class GraphParams:
    @property
    def DB_SERVICE_HOST(self):
        return "DB_service_host"

    @property
    def DB_DATA_QUERY(self):
        return "load_data"

    @property
    def DB_SERVICE_PORT(self):
        return "DB_service_port"

    @property
    def DB_NAME(self):
        return "dbName"

    @property
    def DB_REPLICATION_FACTOR(self):
        return "arangodb_replication_factor"

    @property
    def DB_USER_NAME(self):
        return "username"

    @property
    def DB_PASSWORD(self):
        return "password"
    @property
    def DB_CONN_PROTOCOL(self):
        return "conn_protocol"