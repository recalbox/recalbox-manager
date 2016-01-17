# -*- coding: utf-8 -*-
"""
Support views
"""
from project.api.views import JobView

class TestGitView(JobView):
    """
    Sample that fail
    """
    job_cwd = '.'
    job_args = ('git', 'describe', '.')


class TestLsView(JobView):
    """
    Sample that succeed
    """
    job_cwd = '.'
    job_args = ('ls', '-l', '.')
        
    def job_success(self, job, **kwargs):
        """
        If the job fails, inject response_klass to throw an http code 500 and add message error
        """
        context = super(TestLsView, self).job_success(job, **kwargs)
        context.update({
            'message': job.output.strip(),
        })
        return context
