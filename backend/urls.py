from django.contrib import admin
from django.urls import path
from league import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/bouts/', views.get_todays_bouts, name='todays-bouts'),
    path('api/pebbler/<str:pebblerName>/', views.get_pebbler_info, name='pebbler-info-by-name'),
]
