#!/usr/bin/env python

import cherrypy
import cherrypy_cors
import os
from urls import url_mapper
from mocherry.settings import CONFIG



def runserver(host=None, port=None, threads=None):
    # handle CORS headers
    cherrypy_cors.install()

    # set environment as required
    cherrypy.config.update({
        'global': CONFIG['server']['environment'].lower()
    })

    application = cherrypy.tree.mount(None, config={
        "/": {
            "request.dispatch": url_mapper(),
            'cors.expose.on': True,
            'tools.json_in.force': False
        }
    })

    cherrypy.server.socket_host = CONFIG["server"]["host"]
    cherrypy.server.socket_port = CONFIG["server"]["port"]
    cherrypy.server.thread_pool = CONFIG["server"]["threads"]

    # starting cherrypy wsgi server
    cherrypy.quickstart(application)
