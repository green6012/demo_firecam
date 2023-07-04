from django.urls import path, re_path
from tornado.web import url
from django.conf.urls.static import static
from django.conf import settings
from . import views
app_name = 'realcam'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('warning/', views.warning, name='warning'),

    path('live_camera/<int:camera_id>/', views.live_camera, name='live_camera'),
    path('add_video/',views.add_video, name='add_video'),
    path('delete_camera/<int:camera_id>/',views.delete_camera,name='delete_camera'),
    path('delete_warning/<int:warning_id>/',views.delete_warning,name='delete_warning'),
    path('export_excel', views.export_warnings_to_excel,name='export_excel'),
    path('warnings_search/', views.warnings_search, name='warnings_search'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)