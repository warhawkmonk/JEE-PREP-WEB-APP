from os import name
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('',views.sagar,name="sagar"),
    path('register',views.register,name='register'),
    path('login',views.loginPage,name='login'),
    path('teacher',views.teacher,name='teacher'),
    path('setup',views.setup,name='setup'),
    path('select',views.select,name='select'),
    path('test',views.test,name='test'), 
    path('student',views.student,name='student'),
    path('originaltest',views.originaltest,name='originaltest'),
    path('aftertest',views.aftertest,name='aftertest'),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]         
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT) 