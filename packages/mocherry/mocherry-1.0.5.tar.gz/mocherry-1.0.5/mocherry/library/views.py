#!/usr/bin/env python

import cherrypy
from mocherry.settings import CONFIG
from mocherry.library.http import status

class APIViewset():
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def index(self, **kwargs):
        http_method = getattr(self, cherrypy.request.method)
        if cherrypy.request.method in ['POST', 'PUT']: 
            return (http_method)(cherrypy.request, **kwargs)
        else:
            return (http_method)(**kwargs)

    def GET(self, **kwargs):
        return self.send_response(body={
            'error': {
                'message': 'Method not allowed'
            }
        }, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def POST(self, request, **kwargs):
        return self.send_response(body={
            'error': {
                'message': 'Method not allowed'
            }
        }, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def PUT(self, request, **kwargs):
        return self.send_response(body={
            'error': {
                'message': 'Method not allowed'
            }
        }, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def DELETE(self, **kwargs):
        return self.send_response(body={
            'error': {
                'message': 'Method not allowed'
            }
        }, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)


    def OPTIONS(self, **kwargs):
        if 'cors' in CONFIG['general'] and \
            'host' in CONFIG['general']['cors']:
            cherrypy.response.headers['Access-Control-Allow-Origin'] = CONFIG['general']['cors']['host']
            cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'
            cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Cache-Control, X-Auth-Token, X-Company, Access-Control-Request-Method, Access-Control-Request-Headers'
            cherrypy.response.headers['Allow'] = 'GET, PUT, POST, DELETE, OPTIONS'
        
        return {
            'Allow': 'GET, PUT, POST, DELETE, OPTIONS'
        }

    def send_response(self, body={}, status_code=200):
        cherrypy.response.status = status_code
        cherrypy.response.headers['Content-type'] = 'application/json'
        return body
