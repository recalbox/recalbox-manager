import os, glob, re

from django.shortcuts import render
from django.views.generic import TemplateView

def process_list():

    pids = []
    for subdir in os.listdir('/proc'):
        if subdir.isdigit():
            pids.append(subdir)

    return pids

class HomeView(TemplateView):
    """
    System infos mining is disabled since it's very hard to get all the 
    right stuff. Recommend to use a library like https://pypi.python.org/pypi/psutil
    """
    template_name = "manager_frontend/home.html"
    devices_pattern = ['sd.*','mmcblk*']
    
    #def get_context_data(self, **kwargs):
        #context = super(HomeView, self).get_context_data(**kwargs)
        #context.update({
            #'cpu_infos': self.get_cpu_infos(),
            #'processes_infos': self.get_processes_infos(),
            #'memory_infos': self.get_memory_infos(),
            #'disk_infos': self.get_disk_infos(),
        #})
        
        #return context
    
    #def get_cpu_infos(self):
        #"""
        #TODO: Need a proper way to find cpu usage
        #"""
        #content = {}
        #return content
    
    #def get_processes_infos(self):
        #"""
        #Watch in '/proc' directory to find how many process is running
        #"""
        #pids = []
        #for subdir in os.listdir('/proc'):
            #if subdir.isdigit():
                #pids.append(subdir)
        
        #return {'running': len(pids)}
    
    #def get_memory_infos(self):
        #"""
        #Open '/proc/meminfo' to get usefull infos about memory usage
        #"""
        #content = {}
        #labels = {'MemTotal': 'total','MemFree': 'free'}
        
        #with open('/proc/meminfo') as f:
            #for line in f:
                #key = line.split(':')[0]
                #if key in ('MemTotal','MemFree',):
                    ## Use a better label and convert value in Kb to bytes
                    #value = line.split(':')[1].strip().split(' ')[0]
                    #content[labels[key]] = int(value)*1024
        
        #return content

    #def device_size(self, device):
        #"""
        #Return device size (total or used?)
        #"""
        #nr_sectors = open(device+'/size').read().rstrip('\n')
        #sect_size = open(device+'/queue/hw_sector_size').read().rstrip('\n')

        #return float(nr_sectors)*float(sect_size)

    #def get_disk_infos(self):
        #"""
        #Watch through '/sys/block/*' to find FS devices, filtering them using the 
        #'devices_pattern' class attribute
        #"""
        #content = {}
        #for device in glob.glob('/sys/block/*'):
            #for pattern in self.devices_pattern:
                #if re.compile(pattern).match(os.path.basename(device)):
                    #content[device] = self.device_size(device)
        #return content
