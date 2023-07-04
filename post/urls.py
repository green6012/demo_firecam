
from django.urls import path, include

from post import views
app_name = 'post'
urlpatterns = [

    path('',views.post, name = 'home'),
    path('<int:id>/', views.postDetail, name = 'postDetail')

]