#!/usr/bin/env python

import requests
import json

####################
###
### mist.py
###
### Python wrapper for interacting with the Mist API
### Written by Felix Windt and Bryan Ward, 2019-2020
###
### Version 20200308
###
####################

class Mist:
    def __init__(self, token, org_id, version="v1", ignore_failures=False):
        self.token = token
        self.org_id = org_id
        self.headers = {"Authorization": "Token {0}".format(self.token), "Content-type": "application/json"}
        self.base_url = "https://api.mist.com/api"
        self.version = version
        self.ignore_failures = ignore_failures


    def _constructURL(self, url):
        return self.base_url + "/" + self.version + "/" + url.lstrip("/")


    def _interact(self, method, url, payload=None):
        if payload:
            payload = json.dumps(payload)
        func = getattr(requests, method)
        self.last_reply = func(self._constructURL(url), data=payload, headers=self.headers)
        if self.last_reply.status_code in [200, 201, 202]:
            return self.last_reply.json()
        elif self.last_reply.status_code == 204:
            return True
        elif self.last_reply.status_code in [400, 404, 405, 500, 502, 503]:
            if self.ignore_failures:
                return False
            else:
                raise Exception("HTTP {0}: {1}".format(self.last_reply.status_code, self.last_reply.text))
        else:
            raise Exception("HTTP {0}: {1}".format(self.last_reply.status_code, self.last_reply.text))


    def ignore_failures(self, value):
        self.ignore_failure = value
        return True


    def last_reply(self):
        return self.last_reply


    def get(self, url, payload=None):
        return self._interact("get", url, payload)


    def post(self, url, payload=None):
        return self._interact("post", url, payload)


    def put(self, url, payload=None):
        return self._interact("put", url, payload)


    def delete(self, url, payload=None):
        return self._interact("delete", url, payload)

    def get_self(self):
        myself = self.get("self")
        return myself

    def test_connection(self):
        myself = self.get_self()
        if self.org_id in myself['privileges'][0]['org_id']:
            return True
        return False


