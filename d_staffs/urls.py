from django.urls import path

from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    path('check_application/<str:application_id>', views.check_application, name="staff_check_application"),
        
    path('courses/', views.courses, name="courses"),
    path('edit_course/<str:course_id>', views.edit_courses, name="staff_edit_course"),
    path('create_course/', views.create_courses, name="staff_create_course"),

    # path('careers/', views.home, name="careers"),
    # path('careers/<str:career_id>', views.checkout_career, name="careers"),

]
