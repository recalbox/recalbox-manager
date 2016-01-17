"""
Some common class based views
"""
import json

from django.http import HttpResponse

class JsonMixin(object):
    """
    Mixin containing a 'json_response' method to use instead of common 
    'render_to_response' to return a proper JSON response
    """
    def json_response(self, backend, response_klass=None):
        """
        Attempt a JSON string as the backend
        
        If not a string, assume this is an object suitable to JSON and convert 
        it with json.dumps(...)
        
        Return a response with right content_type and some cache control
        headers (to avoid response caching). 
        
        Default behavior is to return an HttpResponse but if argument 
        'response_klass' is given it should be a Class inherited from 
        HttpResponse and it will be returned.
        """
        if response_klass is None:
            response_klass = HttpResponse
            
        if not isinstance(backend, basestring):
            backend = json.dumps(backend)
        
        content_type = "application/json; charset=utf-8"
        
        response = response_klass(backend, content_type=content_type)
        
        response['Pragma'] = "no-cache"
        response['Cache-Control'] = "no-cache, no-store, must-revalidate, max-age=0" 
        
        return response
