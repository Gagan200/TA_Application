from django.urls import path

from . import views
urlpatterns = [
    path('', views.home, name="home"),
    
    path('course/', views.home, name="course"),
    path('course/<str:course_id>/', views.checkout_course, name="course"),
    
    path('submitions/', views.submitions, name="submitions"),
]
