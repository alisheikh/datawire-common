from proton.handlers import CHandshaker
from linker import Config, Linker

def ancestors(address):
    yield address
    if address is None: return
    address = address.split("?", 1)[0]
    path = address.split("/")[:-1]
    while path:
        addr = "/".join(path)
        yield "%s/" % addr
        yield addr
        path.pop()

class Container:

    def __init__(self, root=None):
        self.root = root
        self.nodes = {}
        self.links = []
        self.handlers = [CHandshaker()]

    def __setitem__(self, address, handler):
        self.nodes[address] = handler

    def __getitem__(self, address):
        for prefix in ancestors(address):
            if prefix in self.nodes:
                return self.nodes[prefix]
        return self.root

    def link(self, config, **kwargs):
        a = Config(config)
        node = self[a.local]
        l = Linker(a, node, **kwargs)
        self.links.append(l)
        return l

    def start(self, reactor):
        for l in self.links:
            l.start(reactor)

    def stop(self, reactor):
        for l in self.links:
            l.stop(reactor)

    def on_link_remote_open(self, event):
        link = event.link
        if link.is_sender:
            address = link.remote_source.address
        else:
            address = link.remote_target.address
        link.handler = self[address]
        if link.handler:
            event.dispatch(link.handler)

    def on_reactor_quiesced(self, event):
        event.dispatch(self.root)
        for h in self.nodes.values():
            event.dispatch(h)

    def on_transport_closed(self, event):
        event.connection.free()

# add link/route/incoming/outgoing?

# container.link(...)
# container.route(...)

# origin.to("//foo/bar")
# origin.from("//foo/bar")
