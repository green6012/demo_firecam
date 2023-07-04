
from django.urls import path, include

from userMember import views
app_name = 'userMember'
urlpatterns = [

    # path('register/',views.registerUser.as_view(), name='registerUser'),
    path('register/',views.register, name = 'registerUser'),
    # path('login/', views.loginUser.as_view(), name='loginUser'),
    path('login/', views.loginPage, name='loginUser'),
    path('logout/',views.logoutUser, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password', views.PasswordChangeView.as_view(template_name='userMember/change_password.html'),name='change_password'),
    path('change_success', views.password_success,name='change_success')
    # path('private/',views.privateWeb, name='private')

]