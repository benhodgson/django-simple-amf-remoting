import re

from amfast.remoting import Service, CallableTarget
from amfast.remoting.channel import ChannelSet
from amfast.remoting.django_channel import DjangoChannel

__all__ = ['SimpleService']

class SimpleService(Service):
    """
    An AMF Service class designed to circumvent the need for repeating the
    boilerplate code that AmFast requires. Get started in three steps:
    
    1) Instantiate a SimpleService with a name:

        >>> math_service = SimpleService('math')
        
    2) Define the callables that you want to expose through the service:
    
        >>> @math_service.expose
        ... def multiply(a, b):
        ...     return a * b
        ...
        
        By default, the name of the method is used for the name of the exposed
        method, although this can be overridden:
        
        >>> @math_service.expose('product')
        ... def multiply(a, b):
        ...     return a * b
        ...
        
    3) Map a URL to the service in your Django urlconf:
    
        >>> from django.conf.urls.defaults import *
        >>> urlpatterns = patterns('',
        ...     url(r'^math/$', math_service),
        ... )
    
    """
    
    VALID_FUNCTION_NAME_RE = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')
    
    def __init__(self, name, channel_name=None, *args, **kwargs):
        
        super(SimpleService, self).__init__(name, *args, **kwargs)
        self.channel = DjangoChannel(channel_name or name)
        self.channel_set = ChannelSet()
        self.channel_set.mapChannel(self.channel)
        self.channel_set.service_mapper.mapService(self)
        
    
    def __call__(self, *args, **kwargs):
        """
        SimpleService instances are callable in such a way that they can be
        used as Django views. When called, they simply delegate to the
        underlying DjangoChannel.
        
        """
        return self.channel(*args, **kwargs)
        
    
    def expose(self, name_or_function=None):
        """A decorator for exposing a callable as a service endpoint."""
        
        def _map_target(function, name=None):
            if name is None:
                # If no name is supplied, use the function name
                name = getattr(function, '__name__', '')                    
            if self.VALID_FUNCTION_NAME_RE.match(name) is None:
                # Check that function name is valid (lambda functions without
                # a supplied name will fail this test)
                raise ValueError("'%s' is not a valid target name" % name)
            self.mapTarget(CallableTarget(function, name))
                
        if callable(name_or_function):
            _map_target(name_or_function)
            return name_or_function
        else:
            def decorator(function):
                _map_target(function, name_or_function)
                return function
            return decorator
    
