
from django.urls import path, include

from polls import views
app_name = 'polls'
urlpatterns = [

    path('home/',views.index, name = 'home'),

    path('news/', views.news, name='news'),
    path('privacy/', views.privacy, name='privacy'),
    path('question/', views.question, name='question'),

]