# Copyright 2015 datawire. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class Common:

    @property
    def version(self):
        import os
        path = os.path.join(os.path.dirname(__file__), "datawire/__init__.py")
        with open(path) as f:
            for line in f:
                if "__version__" in line:
                    g = {}
                    l = {}
                    exec line in g, l
                    return l["__version__"]
        return None

    def setup(self, env):
        env.system("git archive --format=tar --prefix=datawire/ HEAD | (cd %s && tar -xf -)" % env.work)

    def install_prep(self):
        return """
set -e
cd datawire
mkdir -p /work/install/opt/datawire/lib
mkdir -p /work/install/usr/bin
"""

    def install_script(self, script):
        return """
cp %(script)s /work/install/opt/datawire/lib
sed -i -e '1s@.*@#!/usr/bin/python2.7 -u@' /work/install/opt/datawire/lib/%(script)s
cat > /work/install/usr/bin/%(script)s <<LAUNCHER
#!/bin/bash
export PYTHONPATH=/opt/datawire/lib/proton/bindings/python
exec /opt/datawire/lib/%(script)s "\$@"
LAUNCHER
chmod a+x /work/install/usr/bin/%(script)s
""" % {"script": script}

    def install_config(self, dir, system=None):
        if system == "fedora":
            system = "centos"
        result = """
cp -r deploy/%(dir)s/common/* /work/install
"""
        if system:
            result += """
cp -r deploy/%(dir)s/%(system)s-*/* /work/install
"""
        return result % {"system": system or None, "dir": dir}
