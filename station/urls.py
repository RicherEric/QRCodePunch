from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, add_station, add_checkpoint, delete_station, delete_checkpoint, scan_qrcode

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),  # 首页
    path('stations/', views.station_list, name='station_list'),
    path('stations/<int:pk>/', views.station_detail, name='station_detail'),
    path('add-station/', add_station, name='add_station'),
    path('add-checkpoint/', add_checkpoint, name='add_checkpoint'),
    path('delete-station/<int:pk>/', delete_station, name='delete_station'),
    path('delete-checkpoint/<int:pk>/', delete_checkpoint, name='delete_checkpoint'),
    path('scan/<int:checkpoint_id>/', scan_qrcode, name='scan_qrcode')
]