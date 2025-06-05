from django.contrib import admin
from django.urls import path
from league import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/bouts/', views.get_todays_bouts, name='todays-bouts'),
    path('api/bouts/<str:pebblerName>/', views.get_pebbler_bouts, name='pebbler-bouts'),
    path('api/basic/<str:pebblerName>/', views.get_pebbler_basic_info, name='pebbler-basic'),
    path('api/history/<str:pebblerName>/', views.get_performance_history, name='pebbler-history'),
    path('api/personal/<str:pebblerName>/', views.get_pebbler_personal_info, name='pebbler-personal'),
    path('api/rankings/<int:month>/<int:year>/', views.get_ranked_performances, name='performance-by-month'),
]
