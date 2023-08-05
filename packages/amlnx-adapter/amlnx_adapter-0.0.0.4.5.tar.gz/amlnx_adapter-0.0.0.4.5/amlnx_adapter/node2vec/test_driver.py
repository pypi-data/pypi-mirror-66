#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 08:40:37 2020

@author: Rajiv Sambasivan
"""


from amlnx_adapter.graph_params import GraphParams
from amlnx_adapter.node2vec.imdb_networkx_arango_adapter import IMDB_Networkx_Arango_Adapter

def test_conn():
    gp = GraphParams()
    cfg = {}
    cfg[gp.DB_USER_NAME] = "TUTm28hjlz0yplj1kw3gfl7jo"
    cfg[gp.DB_NAME] = "TUTnfa1xuleb5sff8nk2xfas"
    cfg[gp.DB_CONN_PROTOCOL] = 'https'
    cfg[gp.DB_PASSWORD] = 'TUTvne5vnutk7qncfh2f7vlr'
    cfg[gp.DB_SERVICE_HOST] = '5904e8d8a65f.arangodb.cloud'
    cfg[gp.DB_DATA_QUERY] = "FOR ratings in Ratings \
            return {'user': ratings._from, 'movie': ratings._to, 'rating': ratings.ratings}"
    
    ma = IMDB_Networkx_Arango_Adapter(graph_config = cfg)
    g = ma.create_networkx_graph()
    
    return g

def test_conn2():
    ma = IMDB_Networkx_Arango_Adapter()
    g = ma.create_networkx_graph()
    return g