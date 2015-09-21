"""
Monitoring views
"""
from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView

# Compatibility support for Recalbox versions from 3.2.x to 3.3.x
# (psutil package only available since 3.3.0 beta 5)
try:
    import psutil
except ImportError:
    class RecalboxSystemInfosMixin(object):
        psutil_available = False
else:
    class RecalboxSystemInfosMixin(object):
        """
        Mixin to get all system infos using 'psutil' library
        """
        psutil_available = True
        mining_cpu_interval = settings.RECALBOX_PSUTIL_CPU_INTERVAL
        
        def get_cpu_infos(self):
            return {
                'count': psutil.cpu_count(),
                'usage': psutil.cpu_percent(interval=self.mining_cpu_interval, percpu=True),
            }
        
        def get_memory_infos(self):
            virtual_mem = psutil.virtual_memory()
            return {
                'usage_percent': virtual_mem.percent,
                'usage_bytes': virtual_mem.used,
                'free_unified': virtual_mem.available,
                'total': virtual_mem.total,
            }
        
        def get_filesystem_infos(self):
            context = []
            
            for disk_part in psutil.disk_partitions():
                usage = psutil.disk_usage(disk_part.mountpoint)
                context.append({
                    'device': disk_part.device,
                    'mountpoint': disk_part.mountpoint,
                    'fstype': disk_part.fstype,
                    'total': usage.total,
                    'free': usage.free,
                    'used_bytes': usage.used,
                    'used_percent': usage.percent,
                })
            
            return context

class MonitoringView(RecalboxSystemInfosMixin, TemplateView):
    """
    Monitoring view to display system informations
    """
    template_name = "manager_frontend/monitoring.html"
    
    def get_context_data(self, **kwargs):
        context = super(MonitoringView, self).get_context_data(**kwargs)
        context['PSUTIL_AVAILABLE'] = self.psutil_available
        
        if self.psutil_available:
            context.update({
                'cpu_infos': self.get_cpu_infos(),
                'memory_infos': self.get_memory_infos(),
                'filesystem_infos': self.get_filesystem_infos(),
            })
        return context
