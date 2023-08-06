import time
import os
import lockfile
import psutil
from daemon import daemon
from setproctitle import setproctitle
from corens.txt import nsTxt
from corens.ns import *
from corens.console import nsConsole, nsconsole
from corens.env import nsEnvMkPID, nsEnvLoadPid
from corens.mod import lf

def nsDaemonProcTitle(ns, msg=None):
    if msg is None:
        _msg = nsGet(ns, "/etc/processTitle")
        if _msg is None:
            _msg = "core.NS($etc.name) is running on $etc.hostname"
    else:
        _msg = msg
    _msg = nsTxt(ns, _msg)
    setproctitle(_msg)
    return _msg

def nsDaemonMkLock(ns):
    with open("{}.daemon".format(nsGet(ns, "/sys/env/pidFile")), "w") as f:
        f.write(str(os.getpid()))

def nsDaemonCleanUp(ns):
    try:
        os.unlink("{}.daemon".format(nsGet(ns, "/sys/env/pidFile")))
        os.unlink("{}".format(nsGet(ns, "/sys/env/pidFile")))
    except FileNotFoundError:
        return

def nsDaemonLoadPid(ns):
    try:
        with open("{}.daemon".format(nsGet(ns, "/sys/env/pidFile")), "r") as f:
            try:
                pid = int(f.read())
            except ValueError:
                return None
    except FileNotFoundError:
        return None
    try:
        me = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return None
    if me.is_running() is True:
        return pid
    return None

def nsDaemonMain(ns, *args, **kw):
    f = lf(ns)
    nsDaemonProcTitle(ns)
    nsSet(ns, "/sys/env/pid", os.getpid())
    nsSet(ns, "/sys/env/me", psutil.Process(os.getpid()))
    nsEnvMkPID(ns)
    nsDaemonMkLock(ns)
    nsConsole(ns, "PID      : $sys.env.pid")
    isSystem = nsGet(ns, "/etc/flags/system", False)
    if isSystem is True:
        nsConsole(ns, "LOOP name: /sbin/loop")
        nsDaemonProcTitle(ns, "core.NS($etc.name) eventLoop is running as /sbin/loop")
        f("/sbin/loop")()
    else:
        nsConsole(ns, "LOOP name: /bin/loop")
        nsDaemonProcTitle(ns, "core.NS($etc.name) eventLoop is running as /bin/loop")
        f("/bin/loop")()


def nsDaemonStartInt(ns, *args, **kw):
    with daemon.DaemonContext(
        chroot_directory=None,
        working_directory=nsGet(ns, "/sys/env/apphome"),
        uid=nsGet(ns, "/sys/env/uid"),
        stdout=sys.stdout,
        stderr=sys.stderr,
        prevent_core=True):
        nsDaemonMain(ns, *args, **kw)

def nsDaemonStopInt(ns, *args, **kw):
    if os.path.exists(nsGet(ns, "/sys/env/pidFile")) and os.path.isfile(nsGet(ns, "/sys/env/pidFile")):
        nsconsole(ns, "$sys.env.pidFile exists. Checking.")
        pid = nsEnvLoadPid(ns)
        if pid is None:
            nsconsole(ns, "PID in $sys.env.pidFile is not parseable")
            return
        if psutil.pid_exists(pid) is not True:
            nsconsole(ns, "PID[%d] in $sys.env.pidFile not exists in system"%pid)
            return
        me = psutil.Process(pid)
        if me.is_running():
            nsconsole(ns, "Termnating daemon PID=%d"%pid)
            me.terminate()
        c = 0
        for i in range(5):
            nsconsole(ns, "Wait %s"%("."*i))
            time.sleep(1)
            if me.is_running() is False:
                break
        if me.is_running() is True:
            nsconsole(ns, "Killing daemon PID=%d"%pid)
            me.kill()
        nsDaemonCleanUp(ns)

    else:
        nsconsole(ns, "$sys.env.pidFile do not exists. Is daemon running ?")
