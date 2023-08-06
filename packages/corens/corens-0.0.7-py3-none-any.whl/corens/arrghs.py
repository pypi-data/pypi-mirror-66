import sys
import re
import clint
import os.path
import socket
from fs.opener import open_fs
from fs.errors import CreateFailed
from corens.ns import *
from corens.help import *
from corens.mod import f
from corens.cfg import nsCfgAppendFs, nsCfgListenParse
from corens.console import nsConsole, nsconsole

def nsArgs(ns, args=sys.argv[1:]):
    if len(sys.argv) == 0 or sys.argv[0] == '':
        name = 'corens'
    else:
        name = os.path.basename(sys.argv[0])
    path = "/etc/args"
    nsMkdir(ns, path)
    nsMkdir(ns, "{}/default".format(path))
    nsSet(ns, "{}/default/conf".format(path), [])
    nsSet(ns, "{}/default/bootstrap".format(path), [])
    nsSet(ns, "{}/default/userlib".format(path), [])
    nsSet(ns, "{}/default/listen".format(path), [])
    nsSet(ns, "/etc/argv", [])
    nsSet(ns, "/etc/name", name)
    argv = nsGet(ns, "/etc/argv")
    _args = nsGet(ns, path)
    args = clint.arguments.Args(args, True)
    _path = "{}/default".format(path)
    nsMkdir(ns, path)
    nsMkdir(ns, _path)
    nsMkdir(ns, '/etc/flags')
    isFlag = False
    prev = None
    config_list = []
    while True:
        a = args.pop(0)
        if a is None or isinstance(a, str) is not True:
            break
        if len(a) == 0:
            continue
        if re.match(r'--help', a) is not None:
            if prev is None:
                hpath = "/help/cmd/default"
            else:
                hpath = "/help/cmd/{}".format(prev)
            nsHelp(ns, hpath)
            raise SystemExit
        if re.match(r'\+(.*)', a) is not None and isFlag is False:
            nsSet(ns, "/etc/flags/{}".format(a[1:]), True)
            continue
        if re.match(r'\-(\w+)', a) is not None and isFlag is False:
            nsSet(ns, "/etc/flags/{}".format(a[1:]), False)
            continue
        if re.match(r'--(.*)', a) is not None and isFlag is False:
            isFlag = True
            prev = a[2:].lower()
            continue
        if re.match(r'--(.*)', a) is not None and isFlag is True:
            nsSet(ns, "{}/{}".format(_path, prev), True)
            isFlag = True
            prev = a[2:].lower()
            continue
        if re.match(r'--(.*)', a) is None and isFlag is True:
            prevValue = nsGet(ns, "{}/{}".format(_path, prev))
            if prevValue is None:
                nsSet(ns, "{}/{}".format(_path, prev), a)
            elif prevValue is not None and isinstance(prevValue, list) is not True:
                nsSet(ns, "{}/{}".format(_path, prev), [prevValue, a])
            elif prevValue is not None and isinstance(prevValue, list) is True:
                prevValue.append(a)
            else:
                nsSet(ns, "{}/{}".format(_path, prev), a)
            if prev == "conf":
                config_list.append(a)
            isFlag = False
            continue
        if re.match(r'--(.*)', a) is None and isFlag is False:
            prev = a
            argv.append(a)
            _path = "{}/{}".format(path, a)
            nsMkdir(ns, _path)
            continue
    cfg_files = nsGet(ns, "/config/cfg.files")
    cfg_files += config_list
    userlib = nsGet(ns, "/config/user.library")
    userlib += nsGet(ns, "/etc/args/default/userlib")
    listen_list = nsGet(ns, "/etc/listen")
    for l in nsGet(ns, "/etc/args/default/listen"):
        _name, _listen = nsCfgListenParse(ns, l)
        if _name not in listen_list:
            listen_list[_name] = _listen
    cfg_fs_path = nsGet(ns, "/config/cfg.fs")
    for b in nsGet(ns, "/etc/args/default/bootstrap"):
        nsCfgAppendFs(ns, b)
    nsSet(ns, "/etc/name", nsGet(ns, "/etc/args/default/appname", name))
    nsSet(ns, "/etc/hostname", nsGet(ns, "/etc/args/default/hostname", socket.gethostname()))
    nsSet(ns, "/etc/daemonize", nsGet(ns, "/etc/flags/daemonize", False))
    nsSet(ns, "/etc/console", nsGet(ns, "/etc/flags/console", True))
    nsSet(ns, "/etc/log", nsGet(ns, "/etc/flags/log", True))
    return ns

def nsCmd(ns, *args, **kw):
    argv = nsGet(ns, "/etc/argv", [])
    root = nsGet(ns, "/config/cmd.path")
    kw.update(nsGet(ns, "/config/cmd.kw"))
    out = None
    is_cmd_run = nsGet(ns, "/config/cmd.run")
    if is_cmd_run is True:
        return ns
    for k in argv:
        _args = tuple([out,] + list(args))
        try:
            nsconsole(ns, "CMD executed: {}/{}".format(root, k))
            out = f(ns, "{}/{}".format(root, k))(*_args, **kw)
            nsSet(ns, "/config/cmd.run", True)
        except TypeError:
        #except KeyboardInterrupt:
            nsconsole(ns, "CMD not found: {}/{}".format(root, k))
            nsGlobalError(ns, "Command {}/{} not found".format(root, k))
            continue
    return ns
