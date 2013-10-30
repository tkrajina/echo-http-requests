# -*- coding: utf-8 -*-

import pdb

import json as mod_json
import datetime as mod_datetime

import webapp2 as mod_webapp2
import google.appengine.ext.db as mod_db

def to_json(dictionary):
    return mod_json.dumps(dictionary, sort_keys=True, indent=4)

def remove_old():
    dt = mod_datetime.datetime.now()
    dt = dt - mod_datetime.timedelta(minutes=15)
    http_requests = mod_db.GqlQuery('select * from HttpRequest where created < :1', dt)
    n = 0
    for http_request in http_requests:
        http_request.delete()

        n += 1
        if n > 50:
            return

def get_request_id(request):
    url = str(request.url)
    last_part = url.split('/')[-1]
    if '?' in last_part:
        last_part = last_part.split('?')[0]
    return last_part

class HttpRequest(mod_db.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    request_id = mod_db.StringProperty()
    method = mod_db.StringProperty()
    headers = mod_db.BlobProperty()
    body = mod_db.BlobProperty()
    url = mod_db.StringProperty()
    query_string = mod_db.StringProperty()
    http_version = mod_db.StringProperty()
    remote_address = mod_db.StringProperty()
    created = mod_db.DateTimeProperty(auto_now_add=True)

class PushRequestsHerePage(mod_webapp2.RequestHandler):

    def _handle_request(self, http_method):
        remove_old()

        headers = {}
        for key, value in self.request.headers.items():
            if 'x-appengine' not in key.lower():
                headers[str(key)] = str(value)

        result = { 'status': 'OK', }

        http_request = HttpRequest()
        http_request.request_id = get_request_id(self.request)
        http_request.method = http_method
        http_request.headers = mod_json.dumps(headers)
        http_request.body = str(self.request.body)
        http_request.url = str(self.request.url)
        http_request.query_string = str(self.request.query_string)
        http_request.http_version = str(self.request.http_version)
        http_request.remote_address = self.request.remote_addr

        http_request.put()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(to_json(result))

    def get(self):
        self._handle_request('GET')

    def post(self):
        self._handle_request('POST')

    def delete(self):
        self._handle_request('DELETE')

    def put(self):
        self._handle_request('PUT')

    def options(self):
        self._handle_request('OPTIONS')

class PullRequestsFromHerePage(mod_webapp2.RequestHandler):

    def get(self):
        remove_old()

        self.response.headers['Content-Type'] = 'application/json'

        result = {'status': 'OK', 'requests': []}

        http_requests = mod_db.GqlQuery('select * from HttpRequest where request_id = :1', get_request_id(self.request))
        n = 0
        for http_request in http_requests:
            try:
                headers = mod_json.loads(http_request.headers)
            except:
                headers = ''
            request = {
                    'method': http_request.method,
                    'headers': headers,
                    'body': http_request.body,
                    'url': http_request.url,
                    'query_string': http_request.query_string,
                    'http_version': http_request.http_version,
                    'created': str(http_request.created),
                    'remote_address': http_request.remote_address,
            }

            result['requests'].append(request)

            http_request.delete()

            n += 1
            if n == 50:
                result['has_more'] = True
                self.response.write(to_json(result))

        result['has_more'] = False
        self.response.write(to_json(result))

routes = [
        ('/push/.*', PushRequestsHerePage),
        ('/pull/.*', PullRequestsFromHerePage),
]

application = mod_webapp2.WSGIApplication(routes)
