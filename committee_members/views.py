from django.shortcuts import render

from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models import Application, Comment

def debug(str):
    print("__________________________")
    print(str)
    print("__________________________")

def is_verified(user):
    return user.is_verified_user

def is_committee_member(user):
    return user.user_type == user.COMMITTEE_MEMBER

@login_required
@user_passes_test(is_committee_member, login_url="/")
@user_passes_test(is_verified, login_url="/not_verified_user/")
def home(request):
    # application_list = Application.objects.all()
    application_list = Application.objects.filter(recommended=True)

    context = {
        'application_list': application_list,
    }
    return render(request, "committee_members/home.html", context)

@login_required
@user_passes_test(is_committee_member, login_url="/")
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
        if "approve" in request.POST:
            application.approve_by(request.user)
            messages.success(request, "Your response was recorded!")

        if "disapprove" in request.POST:
            application.disapprove_by(request.user)
            messages.success(request, "Your response was recorded!")

        if "add_comment" in request.POST:
            message = request.POST.get("message")
            if message:
                new_comment = Comment(message=message, user=request.user, application=application)
                new_comment.save()
                messages.success(request, "Your response was recorded!")

    comment_list = Comment.objects.filter(application=application)
    context = {
        'application': application,
        'comment_list': comment_list,
        'checklist': checklist,
        'completion_percentage': (no_of_checks / 8) * 100,
    }
    return render(request, "committee_members/check_application.html", context)

# Sorry message for not verified users
def not_verified_user(request):
    return render(request, "not_verified_user.html")