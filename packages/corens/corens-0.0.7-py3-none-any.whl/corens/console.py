import gevent
from Cheetah.Template import Template
from clint.textui import indent, puts, colored
from corens.ns import nsGet
from corens.txt import nsTxt


def nsConsole(ns,  msg, **kw):
    _msg = msg % kw
    _msg = nsTxt(ns, _msg)
    if nsGet(ns, "/etc/console") is False:
        return _msg
    q = nsGet(ns, "/sys/console")
    q.put_nowait(_msg)
    return _msg

def nsconsole(ns, msg, **kw):
    _msg = msg % kw
    _msg = nsTxt(ns, _msg)
    try:
        with indent(4, quote=colored.green("|")):
            puts(_msg)
    except ValueError:
        return

def nsConsoleProcess(ns, entries=1):
    q = nsGet(ns, "/sys/console")
    c = 0
    while True:
        if q.qsize() > 0:
            msg = q.get_nowait()
            c += 1
        else:
            break
        with indent(4, quote=colored.green("|")):
            puts(msg)
        if c >= entries:
            break
        gevent.sleep(0.1)

def nsConsoleDaemon(ns):
    while True:
        nsConsoleProcess(ns, 10)
        gevent.sleep(0.1)

def nsConsoleSize(ns):
    q = nsGet(ns, "/sys/console")
    return q.qsize()
