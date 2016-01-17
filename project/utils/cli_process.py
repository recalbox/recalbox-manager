# -*- coding: utf-8 -*-
"""
Usefull stuff for commandline script execution
"""
import subprocess, sys

class ProcessCallerError(Exception):
    pass

class SimpleCaller(object):
    """
    Simple caller for Popen subprocess
    """
    def __init__(self, cwd=None):
        """
        If @cwd is not None, the child’s current directory will be changed to cwd before it is executed
        """
        self.cwd = cwd

    def __call__(self, *args):
        popen = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.cwd)
        out, err = popen.communicate()
        
        if popen.returncode != 0:
            # Raise an exception containing exit code and return error message
            raise ProcessCallerError(u'{code}: {message}'.format(code=popen.returncode, message=err.strip()))
        
        return out

class Job(object):
    """
    Job processor
    
    Try to mimic Django forms behavior
    """
    output = None
    returncode = None
    error = None
    
    def __init__(self, *args, **kwargs):
        """
        If @cwd is not None, the child’s current directory will be changed to cwd before it is executed
        """
        self.args = args # commandline script and arguments
        self.cwd = kwargs.get('cwd', None)

    def execute(self):
        """
        Proceed to job execute
        """
        popen = subprocess.Popen(self.args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.cwd)
        output, error = popen.communicate()
        
        self.returncode = popen.returncode
        self.output = output
        self.error = error.strip()

    def is_success(self):
        """
        Execute job to check if error occured
        """
        self.execute()
        
        if self.returncode != 0:
            return False
        return True
    