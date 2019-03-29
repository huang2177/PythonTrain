from django.urls import path

from mysite.app.views import *

urlpatterns = [
    path('admin/', clazz),
    path('clazz/', clazz),
    path('add_clazz/', add_clazz),
    path('del_clazz/', del_clazz),
    path('edit_clazz/', edit_clazz),

    path('teachers/', teachers),
    
    path('students/', students),
    path('add_student/', add_student),
    path('edit_student/', edit_student),
]
