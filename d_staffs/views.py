from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from core.models import Application, Comment, Course
from admin_users.forms import CourseForm


def debug(str):
    print("__________________________")
    print(str)
    print("__________________________")
    
def is_verified(user):
    return user.is_verified_user

def is_staff(user):
    return user.user_type == user.STAFF

@login_required
@user_passes_test(is_staff, login_url="/")
@user_passes_test(is_verified, login_url="/not_verified_user/")
def home(request): 
    application_list = Application.objects.all()

    context = {
        'application_list': application_list,
    }
    return render(request, "d_staffs/home.html", context)


@login_required
@user_passes_test(is_staff, login_url="/")
@user_passes_test(is_verified, login_url="/not_verified_user/")
def check_application(request, application_id):
    application = Application.objects.get(id=application_id)
    checklist = {
        "Bachelor's degree in a relevant field": application.box1,
        "Prior teaching experience": application.box2,
        "Ability to work collaboratively": application.box3,
        "Organizational skills": application.box4,
        "Certifications and Training": application.box5,
        "Additional Qualifications": application.box6,
        "Personal Statement/Statement of Purpose": application.box7,
        "Proficiency in specific subject areas": application.box8,
    }

    no_of_checks = 0
    if application.box1: no_of_checks += 1
    if application.box2: no_of_checks += 1
    if application.box3: no_of_checks += 1
    if application.box4: no_of_checks += 1
    if application.box5: no_of_checks += 1
    if application.box6: no_of_checks += 1
    if application.box7: no_of_checks += 1
    if application.box8: no_of_checks += 1

    if request.method == "POST":
        if "recommend" in request.POST:
            application.recommended = True
            application.status = Application.RECOMMENDED
            application.save()

        if "add_comment" in request.POST:
            message = request.POST.get("message")
            if message:
                new_comment = Comment(message=message, user=request.user, application=application)
                new_comment.save()
                messages.success(request, "Comment added!")

        if "save_checklist" in request.POST:
            print("____###")
            data = []
            for i in range(8):
                box = request.POST.get(f"box{i+1}")
                if box: data.append(True)
                else: data.append(False)
                
            application.box1 = data[0]
            application.box2 = data[1]
            application.box3 = data[2]
            application.box4 = data[3]
            application.box5 = data[4]
            application.box6 = data[5]
            application.box7 = data[6]
            application.box8 = data[7]
            print(data)
            application.save()
            return redirect(f'/d_staffs/check_application/{application.id}')

    comment_list = Comment.objects.filter(application=application)
    context = {
        'application': application,
        'comment_list': comment_list,
        'checklist': checklist,
        'completion_percentage': (no_of_checks / 8) * 100,
    }
    return render(request, "d_staffs/check_application.html", context)


@login_required
@user_passes_test(is_verified, login_url="/not_verified_user/")
def courses(request):
    course_list = Course.objects.all()

    context = {
        'course_list': course_list,
    }
    return render(request, "d_staffs/courses.html", context)


@login_required
@user_passes_test(is_verified, login_url="/not_verified_user/")
def edit_courses(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("/d_staffs/courses/")

    form = CourseForm(instance=course)
    return render(request, "d_staffs/create_course.html", { 'form': form } )

@login_required
@user_passes_test(is_verified, login_url="/not_verified_user/")
def create_courses(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/d_staffs/")

    form = CourseForm()
    return render(request, "d_staffs/create_course.html", { 'form': form } )
