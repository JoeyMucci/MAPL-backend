from django.contrib import admin
from django.urls import path
from league import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/bouts/<int:month>/<int:day>/<int:year>', views.get_bouts, name='bouts-by-day'),
    path('api/bouts/<str:pebblerName>/<int:month>/<int:year>', views.get_pebbler_bouts, name='pebbler-bouts'),
    path('api/bout/<int:id>/', views.get_bout_by_id, name='specific-bout'),
    path('api/pebblers/basic/<str:pebblerName>/', views.get_pebbler_basic_info, name='pebbler-basic'),
    path('api/pebblers/history/<str:pebblerName>/<int:year>', views.get_performance_history, name='pebbler-history'),
    path('api/pebblers/personal/<str:pebblerName>/', views.get_pebbler_personal_info, name='pebbler-personal'),
    path('api/pebblers/summary/<str:pebblerName>/', views.get_pebbler_aggregate, name='pebbler-summary'),
    path('api/rankings/<int:month>/<int:year>/', views.get_ranked_performances, name='performances-by-month'),
]
