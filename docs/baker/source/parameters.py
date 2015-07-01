
def _version():
    import os
    path = os.path.join(os.path.dirname(__file__), "../../../datawire/__init__.py")
    with open(path) as f:
        for line in f:
            if "__version__" in line:
                g = {}
                l = {}
                exec line in g, l
                return l["__version__"]
    return None

version = _version()
repo = "staging"
install = "https://packagecloud.io/datawire/%s/install" % repo
script_rpm = "https://packagecloud.io/install/repositories/datawire/%s/script.rpm.sh" % repo
script_deb = "https://packagecloud.io/install/repositories/datawire/%s/script.deb.sh" % repo