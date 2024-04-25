from django.urls import path

from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    path('check_application/<str:application_id>', views.check_application, name="instructor_check_application"),
]
