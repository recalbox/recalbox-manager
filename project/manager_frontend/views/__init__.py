from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "manager_frontend/home.html"
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        foo = {
            'cpu_infos': self.get_cpu_infos(),
            'memory_infos': self.get_memory_infos(),
            'disk_infos': self.get_disk_infos(),
        }
        context.update(foo)
        
        #import json
        #print json.dumps(foo, indent=4)
        
        return context
    
    def get_cpu_infos(self):
        content = {}
        return content
    
    def get_memory_infos(self):
        content = {}
        
        with open('/proc/meminfo') as f:
            for line in f:
                key = line.split(':')[0]
                if key in ('MemTotal','MemFree',):
                    content[key] = line.split(':')[1].strip()
        
        return content
    
    def get_disk_infos(self):
        content = {}
        return content
