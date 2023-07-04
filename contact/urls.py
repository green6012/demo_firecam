
from django.urls import path
from . import views
app_name = 'contact'
urlpatterns = [

    path('',views.contact.as_view(), name = "contact"),
    # path('getContact/', views.getContact, name = "getContact"),
    # path('saveContact/', views.saveContact, name = 'saveContact')
]