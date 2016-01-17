"""
Support views
"""
from project.api.views import ApiBaseJsonView
from project.utils.cli_process import SimpleCaller

class SupportScriptView(ApiBaseJsonView):
    _default_state = 'pending'
    
    def get(self, request, *args, **kwargs):
        self.call()
        return super(SupportScriptView, self).get(request, *args, **kwargs)
    
    def call(self):
        call = SimpleCaller('.')
        version = call('git', 'describe', '.')
        print version
        return version.strip()
