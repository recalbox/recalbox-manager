from django.conf.urls import url

from .views import SuccessView
from .views.support import SupportScriptView
from .views.toast import TestGitView, TestLsView

urlpatterns = [
    url(r'^ping/$', SuccessView.as_view(), name='ping'),
    
    #url(r'^support/script/$', SupportScriptView.as_view(), name='support-script'),
    
    url(r'^test/git/$', TestGitView.as_view(), name='support-git'),
    url(r'^test/ls/$', TestLsView.as_view(), name='support-ls'),
]