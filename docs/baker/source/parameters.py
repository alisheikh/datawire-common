
def _getvar(var, path, default=None):
    with open(path) as f:
        for line in f:
            if var in line:
                g = {}
                l = {}
                exec line in g, l
                return l[var]
    return default

def _version():
    import os
    return _getvar("__version__", os.path.join(os.path.dirname(__file__),
                                               "../../../datawire/__init__.py"),
                   "X.X")

def _repo():
    import os
    return _getvar("REPO", os.path.join(os.path.dirname(__file__),
                                        "../../../roy.py"), "stable")

version = _version()
repo = _repo()
install = "https://packagecloud.io/datawire/%s/install" % repo
script_rpm = "https://packagecloud.io/install/repositories/datawire/%s/script.rpm.sh" % repo
script_deb = "https://packagecloud.io/install/repositories/datawire/%s/script.deb.sh" % repo
