import uwsgi
import bottle
import threading
import hashlib
import pickle
import gevent
import random

from gevent.timeout import Timeout
from gevent.event import AsyncResult


try:
    import local_config
    allowed_ips = getattr(local_config, "ALLOWED_IPS", ["127.0.0.1"])
    debug = getattr(local_config, "DEBUG", False)
    secret = getattr(local_config, "UWSGI_ID_SECRET", None)
except BaseException as exc:
    print "EventHandler: Could not load local settings, using default! Error: " + str (exc)
    debug = False
    secret = None
    allowed_ips = ["127.0.0.1"]

bottle.debug(debug)


LOCK = threading.Lock()
curEvent = None
newEvent = AsyncResult()


@bottle.post('/demovibes/ajax/monitor/new/')
def http_event_receiver():
    """Serves request sent by HTTP from sockulf."""

    ip = bottle.request.environ.get('REMOTE_ADDR')
    if ip not in allowed_ips:
        print "Rejected IP: " + ip
        return ip

    try:
        data = bottle.request.forms.get('data')
        data = pickle.loads(data)

        event_receiver(data, 0)
    except BaseException as err:
        print "Error handling request through HTTP: " + str (err)

    return "OK"


def event_receiver (obj, id):
    """Used directly by uwsgi to handle events sent by demovibes."""

    global curEvent
    global newEvent

    LOCK.acquire()
    try:
        newEvent.set(obj)

        curEvent = newEvent
        newEvent = AsyncResult()
    finally:
        LOCK.release()


@bottle.get ('/demovibes/ajax/monitor/:id#[0-9]+#/')
def handler (id):
    # Validate user signature
    userid = bottle.request.GET.get ('uid', None)
    if userid and secret:
        hash = hashlib.sha1("%s.%s" % (userid, secret)).hexdigest()
        sign = bottle.request.GET.get ('sign', "NA")
        if hash != sign:
            userid = None

    id = int(id)

    LOCK.acquire()
    try:
        myCurEvent = curEvent
        myNewEvent = newEvent
    finally:
        LOCK.release()

    # Event format: (list of events, recent event id)

    myevent = None

    if myCurEvent is not None:
        myevent = myCurEvent.get(timeout = 1)

    if not myevent or myevent[1] <= id:
        try:
            myevent = myNewEvent.get(timeout = 50 + random.randint(0, 20))
        except Timeout:
            myevent = None

    if not myevent:
        yield ""
    else:
        eventid = myevent[1]
        levent = [x[1] for x in myevent[0] if x[0] > id and (x[2] == "N" or (userid and x[2] == int(userid)))]
        levent = set(levent)

        yield "\n" + "\n".join(levent) + "\n!%s" % eventid


uwsgi.message_manager_marshal = event_receiver
application = bottle.default_app()


#  LocalWords:  EventHandler sockulf uwsgi
