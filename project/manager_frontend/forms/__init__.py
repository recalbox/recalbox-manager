"""
Here we try to safely use crispy_form if installed
"""
from django.utils.translation import ugettext as _

from project.utils.imports import safe_import_module

# Try to import "crispy-forms" base stuff to use for the default helper
try:
    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Submit
except ImportError:
    # Dummy objects when crispy-forms is not available
    def default_helper():
        return None
    class CrispyFormMixin(object): pass
else:
    # Ok, crispy-forms is installed
    def default_helper(form_tag=True):
        helper = FormHelper()
        helper.form_action = '.'
        helper.form_tag = form_tag
        helper.add_input(Submit('submit', _('Submit')))
        return helper

    class CrispyFormMixin(object):
        """
        Embed the technic in a form mixin to use "crispy-forms" and safely fallback if not installed
        
        Mixin attributes that you can define to change behavior :
        
        * crispy_form_helper_path: Python path to the helper;
        * crispy_form_helper_kwargs: Kwargs dict to give to the helper when initialized;
        * crispy_form_tag: A boolean, add <form> tag if True;
        """
        crispy_form_helper_path = None # Custom layout method path
        crispy_form_helper_kwargs = {}
        crispy_form_tag = True
        
        def __init__(self, *args, **kwargs):
            # Specified helper if any (and import succeed)
            helper = safe_import_module(self.crispy_form_helper_path, default=default_helper)
            if helper is not None:
                self.helper = helper(form_tag=self.crispy_form_tag, **self.crispy_form_helper_kwargs)
            else:
                # Default helper
                self.helper = default_helper(form_tag=self.crispy_form_tag)
