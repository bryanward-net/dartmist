# dartmist

A library for interacting with the Mist Systems API

## Requirements

Python libraries

* websocket
* websocket-client

## Installation

    pip3 install dartmist
Will install this library and all required libraries

## Setup

## Environment

You must specify a Mist Org ID and a Mist API Token.  These can be passed in via the command line (see Usage) 
or, preferably, set as envinronment variables:

    export MIST_ORGID="00000000-0000-0000-0000-000000000000"
    export MIST_TOKEN="12345123451234512345123451234512345"

To get an API Token, refer to the documentation provided by Mist [https://api.mist.com/api/v1/docs/Auth#api-token](https://api.mist.com/api/v1/docs/Auth#api-token)

## Usage

In your python script:

    from dartmist import mist, misthelpers
    api = mist.Mist(TOKEN, ORGID)
    helper = misthelpers.MistHelpers(api)

To use the MistWebsocket class:

    import threading
    ev = threading.Event()
    mwsock = mistwebsocket.MistWebsocket(TOKEN, ev)
    mswock.open()
    if ws.is_open:
        print("Yes, the Websocket is open")
    else:
        logging.error("Failed to open Websocket")
        exit(-1)
    mwsock.subscribe()
    while not ev.isSet() and len(ws.messages) == 0:
        logging.debug("Waiting...")
        msg_rcvd = ev.wait(10)
    if msg_rcvd or ev.isSet() or len(ws.messages) > 0:
        # Process messages
        msg = json.loads(ws.get_next_message())
    mwsock.unsubscribe()
    mwsock.close()
