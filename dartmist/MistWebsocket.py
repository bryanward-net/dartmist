#!/usr/bin/env python

import requests
import json
import websocket
import threading
import logging
from . import Mist

####################
###
### mistwebsocket.py
###
### Python wrapper for interacting with the Mist API Websockets
### Written by Bryan Ward, 2020
###
### Version 20200308
###
####################

class MistWebsocket:
    def __init__(self, token, ev, version="v1", ignore_failures=False, trace=False):
        self.token = token
        self.headers = {"Authorization": "Token {0}".format(self.token), "Content-type": "application/json"}
        self.base_url = "wss://api-ws.mist.com/api-ws/{0}/stream".format(version)
        self.version = version
        self.ignore_failures = ignore_failures
        self.is_open = False
        self.messages = []
        self.app = None
        self.wst = None
        self.ev = ev
        if trace:
            websocket.enableTrace(True)


    def subscribe(self, channel="/test"):
        logging.debug("Subscribing to {0}".format(channel))
        self.app.send(json.dumps({"subscribe": channel}))
        return

    def unsubscribe(self, channel="/test"):
        logging.debug("Unsubscribing from {0}".format(channel))
        self.app.send(json.dumps({"unsubscribe": channel}))
        return

    def on_message(self, message):
        logging.debug(message)
        self.messages.append(message)
        self.ev.set()
        return

    def on_error(self, ws, error="Unknown"):
        logging.error(error)
        return

    def on_close(self, *ws):
        logging.debug("Websocket Closed!")
        self.is_open=False
        return

    def on_open(self, *ws):
        logging.debug("Websocket Open!")
        self.is_open = True
        return

    def on_ping(self, *ws):
        logging.debug("PING")
        return

    def on_pong(self, *ws):
        logging.debug("PONG")
        return

    def flush_messages(self):
        self.messages = []
        self.ev.clear()
        logging.debug("Message stack flushed!")
        return

    def get_next_message(self):
        m = None
        m = self.messages.pop(0)
        return m

    def get_latest_message(self):
        m = None
        m = self.messages.pop(-1)
        return m

    def close(self):
        logging.debug("Closing Websocket")
        #self.app.keep_running = False
        self.app.close()
        self.wst.join()
        logging.debug("Websocket Thread Terminated")
        return

    def open(self):
        logging.debug("Opening Websocket...")
        try:
            self.app = websocket.WebSocketApp(self.base_url,
                #header=["Authorization: Basic {0}".format(base64.encodestring(config["ws_username"] + ':' + config["ws_password"]))],
                header = {"Authorization": "Token {0}".format(self.token), "Content-type": "application/json"},
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
                on_open=self.on_open,
                on_ping=self.on_ping,
                on_pong=self.on_pong)
        except Exception as e:
            logging.error(e)
        try:
            logging.debug("Trying to run")
            self.app.keep_running = True
            self.wst = threading.Thread(target=self.app.run_forever, kwargs={"ping_interval":10, "ping_timeout":5}) #"sslopt":{"cert_reqs": ssl.CERT_NONE}
            self.wst.daemon = True
            self.wst.start()
            logging.debug("Websocket Thread Started")
            while not self.app.sock.connected:
                from time import sleep
                sleep(1)
            if self.app.sock.connected:
                logging.debug("Sock Connected")
                #assert self.is_open = True
    

        except Exception as e:
            logging.error(e)
        return
