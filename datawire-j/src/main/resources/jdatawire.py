
# Probable interaction with python io package...
# in some cases the io.datawire package later gets removed, so grab references to stuff needed at runtime

from io.datawire import Address
from io.datawire import Counts
from io.datawire import Processor as io_datawire_Processor
from io.datawire import Decoder as io_datawire_Decoder
from io.datawire import Sampler as io_datawire_Sampler
from io.datawire import Event
from io.datawire.impl import EventImpl as io_datawire_impl_EventImpl

from proton import WrappedHandler, _chandler
from org.apache.qpid.proton.engine import BaseHandler

from proton import Event as proton_Event
from proton import Message as proton_Message

class NamedProperty(object):
    _fullname = None
    _name = None

    def __get__(self, instance, clazz = None):
        if instance is None:
            return self
        if self._name is None:
            self._name = self.myname(clazz or instance.__class__)
        return self.get(instance)

    def myname(self, clazz):
        for clz in clazz.__mro__:
            for name, value in clz.__dict__.iteritems():
                if value is self:
                    self._fullname = clz.__module__ + "." + clz.__name__ + "." + name
                    return name
        return "*unknown*"

    def get(self, instance):
        raise AttributeError(self._fullname + " did not implement get()")

class ExtendedProperty(NamedProperty):
    def __init__(self, accessor, converter):
        self.accessor = accessor
        self.converter = converter

    def get(self, instance):
        record = vars(instance).get("_record", None)
        if record is None:
            raise AttributeError(self._name + " has no _record")
        value = self.accessor.get(record)
        if value is None:
            raise AttributeError(self._name + " is not in record")
        converted = self.converter(value)
        instance.__dict__[self._name] = converted
        return converted

class NamedSettableProperty(NamedProperty):
    def __set__(self, instance, value):
        if self._name is None:
            self._name = self.myname(instance.__class__)
        self.set(instance, value)

    def set(self, instance, value):
        raise AttributeError(self._fullname + " did not implement set()")

class WrappedHandlerProperty(NamedSettableProperty):
    def get(self, instance):
        return getattr(instance._impl, self._name)

    def set(self, instance, value):
        setattr(instance._impl, self._name, value)

def wrap_proton_message(impl):
    wrapper = proton_Message()
    wrapper._msg.decode(impl)
    wrapper._post_decode()
    return wrapper

proton_Event.message = ExtendedProperty(io_datawire_impl_EventImpl.MESSAGE, wrap_proton_message)


def unwrap_handler(delegate):
    if delegate is not None:
        if isinstance(delegate, BaseHandler):
            return delegate
        else:
            return _chandler(delegate)
    else:
        return None

class Decoder(WrappedHandler):

    def __init__(self, delegate = None):
        def datawire_decoder():
            args = []
            args.append(unwrap_handler(delegate))
            return io_datawire_Decoder(*args)
        WrappedHandler.__init__(self, datawire_decoder)

class Processor(WrappedHandler):

    def __init__(self, delegate = None, window = None):
        def datawire_processor():
            args = []
            args.append(unwrap_handler(delegate))
            if window is not None:
                args.append(window)
            ret = io_datawire_Processor(*args)
            return ret
        WrappedHandler.__init__(self, datawire_processor)

class Sampler(WrappedHandler):

    def __init__(self, delegate = None, frequency = None):
        def datawire_sampler():
            args = []
            args.append(unwrap_handler(delegate))
            if frequency is not None:
                args.append(frequency)
            return io_datawire_Sampler(*args)

        WrappedHandler.__init__(self, datawire_sampler())

    frequency = WrappedHandlerProperty()

class Impls:
    Address = Address
    Decoder = Decoder
    Processor = Processor
    Sampler = Sampler
    Counts = Counts

impls = Impls()
del Impls