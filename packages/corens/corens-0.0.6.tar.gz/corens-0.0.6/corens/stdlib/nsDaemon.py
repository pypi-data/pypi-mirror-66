import time
import psutil
from corens.console import nsConsole, nsconsole
from corens.daemon import *
from corens.ns import *
from corens.mod import lf
from corens.env import nsEnvLoadPid

def nsDaemonStart(ns, *args, **kw):
    f = lf(ns)
    V = f("V")
    if V("/etc/daemonize") is False:
        nsConsole(ns, "No can do: +daemonize is not requested.")
        return
    pid = nsDaemonLoadPid(ns)
    if pid is not None:
        nsconsole(ns, "Application already daemonized. No can do.")
        return
    nsConsole(ns, "Starting core.NS($etc.name) daemon")
    nsConsole(ns, "APP  name: $etc.name")
    nsConsole(ns, "HOST name: $etc.hostname")
    nsConsole(ns, "PID  file: $sys.env.pidFile")
    f("/usr/local/bin/_start")(*args, **kw)

def nsDaemonStop(ns, *args, **kw):
    nsconsole(ns, "Stop requested")
    f = lf(ns)
    V = f("V")
    if V("/etc/daemonize") is True:
        nsconsole(ns, "No can do: +daemonize is requested.")
        return
    f("/usr/local/bin/_stop")(*args, **kw)


def nsDaemonStatus(ns, *args, **kw):
    f = lf(ns)
    V = f("V")
    pid = nsEnvLoadPid(ns)
    if pid is None:
        nsconsole(ns, "No process was found")
        nsDaemonCleanUp(ns)
        return
    me = psutil.Process(pid)
    if me.is_running() is True:
        nsconsole(ns, "Process is running with PID %d"%pid)
    else:
        nsconsole(ns, "Process is not running")
        nsDaemonCleanUp(ns)


_lib = {
    '/bin/setproctitle': nsDaemonProcTitle,
    '/usr/local/bin/start': nsDaemonStart,
    '/usr/local/bin/_start': nsDaemonStartInt,
    '/usr/local/bin/stop': nsDaemonStop,
    '/usr/local/bin/_stop': nsDaemonStopInt,
    '/usr/local/bin/status': nsDaemonStatus,
}
