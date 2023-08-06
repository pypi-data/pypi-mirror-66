from corens.ns import *
from corens.tpl import nsMk

def nsVNSinit(ns, *args, **kw):
    nsSet(ns, "/etc/fstab", {})
    nsMk(ns, "disk")
    return ns

def nsVNSRegister(ns, name, **kw):
    fstab = V(ns, "/etc/fstab")
    if name in fstab:
        return fstab[name]
    if 'type' not in kw:
        return None
    fstab[name] = kw
    return kw

def nsVNSget(ns, name):
    fstab = V(ns, "/etc/fstab")
    return fstab.get(name, None)
