from django.contrib import admin
from django.urls import path
from league import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/bouts/', views.get_todays_bouts, name='todays-bouts'),
]
