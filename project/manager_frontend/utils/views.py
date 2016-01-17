"""
Some common class based views
"""
import json

from django.views.generic.edit import TemplateResponseMixin, FormMixin, ProcessFormView

class MultiFormView(TemplateResponseMixin, FormMixin, ProcessFormView):
    """
    This is a huge rewrite and mixing of some CBV views and mixins to be able 
    to distinctly manage multiple forms in the same view
    
    The view can implement some custom method for some forms that will be used 
    during ProcessFormView process.
    
    Forms have to implement a 'form_key' and 'form_fieldname_trigger' 
    attributes.
    
    The first is the key name to use to build form object name (in view 
    context) and build optional custom view methods. 
    
    The second is the name attribute of the input watched to know if the form 
    is triggered like with a submit button.
    
    Both must be unique through the forms of the view.
    
    TODO: This view should implement some warnings about needed stuff like 
          form attributes and form object names if not defined. So actually 
          you'll have to remember of this yourself.
    """
    # The patterns used to find method/names from form 'form_key' attribute
    getformkwargs_pattern = 'get_{}_form_kwargs'
    formvalid_pattern = '{}_form_valid'
    formobject_pattern = '{}_form'
    
    def get_form(self, form_class=None, empty=False):
        """
        Returns an instance of the form to be used in this view.
        
        Modified to give the 'form_class' to 'get_form_kwargs' and accept 'empty' arg
        """
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs(form_class, empty=empty))
    
    def get_form_kwargs(self, form_class=None, empty=False):
        """
        Returns the keyword arguments for instantiating the form. Basically the 
        kwargs are the same for all forms.
        
        Accept 'form_class' and 'empty' optionnal args
        
        'empty' argument purpose is to enforce unbound form (so only the triggered 
        form is bound)
        
        In the end, try to use the custom method 'get_KEY_form_kwargs' for the 
        given form where 'KEY' is the form 'form_key' attribute. The method is 
        given the current kwargs and must return it (modified or not)
        """
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if not empty and self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        
        # Try custom form method
        if form_class:
            form_key = form_class.form_key
            if hasattr(self, self.getformkwargs_pattern.format(form_key)):
                kwargs = getattr(self, self.getformkwargs_pattern.format(form_key))(kwargs)
        
        return kwargs

    def form_valid(self, form):
        """
        Use the custom form method if any, returns either the custom form method return if 
        not None or the default View response
        """
        form_key = form.form_key
        if hasattr(self, self.formvalid_pattern.format(form_key)):
            resp = getattr(self, self.formvalid_pattern.format(form_key))(form)
            # If the XXX_form_valid method does not return None, assume it's a Response
            if resp is not None:
                return resp
            
        return super(MultiFormView, self).form_valid(form)

    def form_invalid(self, *args):
        """
        Fill context with all given forms
        """
        forms = {}
        for form in args:
            key = self.formobject_pattern.format(form.form_key)
            forms[key] = form
        
        return self.render_to_response(self.get_context_data(**forms))
        
    def get(self, request, *args, **kwargs):
        """
        Just initialize enabled forms as unbounded
        """
        # Add all enabled forms to the view context as initialized 
        # unbounded form
        forms = {}
        for form_class in self.enabled_forms:
            key = self.formobject_pattern.format(form_class.form_key)
            forms[key] = self.get_form(form_class)
        
        return self.render_to_response(self.get_context_data(**forms))
    
    def post(self, request, *args, **kwargs):
        """
        Initialize enabled forms but only the one its submit is triggered will 
        be bounded, other are still unbounded
        """
        forms = []
        triggered_form = None
        for form_class in self.enabled_forms:
            # From default, forms are all empty but the triggered one
            empty = True
            if self.request.POST.get(form_class.form_fieldname_trigger):
                empty = False
            # Init form and append it
            form_instance = self.get_form(form_class, empty=empty)
            forms.append(form_instance)
            # Retain the triggered
            if self.request.POST.get(form_class.form_fieldname_trigger):
                triggered_form = form_instance
        
        # Check if triggered form is valid or not
        if triggered_form and triggered_form.is_valid():
            return self.form_valid(triggered_form)
        else:
            return self.form_invalid(*forms)
