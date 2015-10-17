"""
Views for logs files
"""
from django.conf import settings
from django.views.generic import TemplateView

class LogsView(TemplateView):
    template_name = "manager_frontend/logs_detail.html"
            
    def get_logs_file(self):
        content = None
        
        with open(settings.RECALBOX_LOGFILE_PATH, 'rb') as file:
            content = file.read()
            
        return content
    
    def get_context_data(self, **kwargs):
        context = super(LogsView, self).get_context_data(**kwargs)
        context.update({
            'logs_filepath': settings.RECALBOX_LOGFILE_PATH,
            'logs_content': self.get_logs_file(),
        })
        return context
