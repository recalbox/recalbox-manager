"""
Base views
"""
from django.views.generic.base import View
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseServerError

from project.utils.views import JsonMixin
from project.utils.cli_process import Job

class ApiBaseJsonView(JsonMixin, View):
    """
    Base API JSON view
    """
    default_job_state = None # Default returned state is null, inheritor should define it
    
    def get_job_state(self):
        return self.default_job_state
    
    def get_context_data(self, **kwargs):
        if 'state' not in kwargs:
            kwargs['state'] = self.get_job_state()
        return kwargs
    
    def get(self, request, *args, **kwargs):
        response_klass = kwargs.pop('response_klass', None)
        
        context = self.get_context_data(**kwargs)
        
        return self.json_response(context, response_klass=response_klass)


class SuccessView(ApiBaseJsonView):
    """
    Very simple view that dont do anything and always return success
    """
    default_job_state = 'success'


class JobView(ApiBaseJsonView):
    """
    Base API Json view to execute commands
    """
    default_job_state = 'pending'
    job_class = Job
    job_args = None # TODO: raise an exception if not correctly setted
    job_cwd = None

    def get_job_class(self):
        """
        Returns the job class to use in this view
        """
        return self.job_class

    def get_job(self, job_class=None):
        """
        Returns an instance of the job to be used in this view.
        """
        if job_class is None:
            job_class = self.get_job_class()
        return job_class(*self.get_job_args(), **self.get_job_kwargs())
    
    def get_job_args(self):
        if self.job_args is None:
            raise ImproperlyConfigured("JobView requires attribute 'job_args' to be filled (not None)")
        return self.job_args

    def get_job_kwargs(self):
        """
        Returns the keyword arguments for instantiating the job.
        """
        return {
            'cwd': self.job_cwd,
        }
    
    def job_success(self, job, **kwargs):
        return kwargs

    def job_fail(self, job, **kwargs):
        """
        If the job fails, inject response_klass to throw an http code 500 and add message error
        """
        kwargs.update({
            'response_klass': HttpResponseServerError,
            'state':'error',
            'message': job.error,
        })
        return kwargs
    
    def get(self, request, *args, **kwargs):
        job = self.get_job()
        
        if job.is_success():
            kwargs = self.job_success(job, **kwargs)
        else:
            kwargs = self.job_fail(job, **kwargs)
        
        return super(JobView, self).get(request, *args, **kwargs)
