from django.shortcuts import render

from .models import Application, Course
from django.contrib import messages
from .forms import  ApplicationForm
from django.contrib.auth.decorators import login_required

def debug(str):
    print("__________________________")
    print(str)
    print("__________________________")

@login_required
def home(request):
    course_list = Course.objects.all()

    context = {
        'course_list': course_list,
    }
    return render(request, "list_of_applications.html", context)


@login_required
def checkout_course(request, course_id):
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        debug(form)
        if form.is_valid():
            new_application = form.save(commit=False)
            new_application.user = request.user
            new_application.save()
            messages.success(request, "Thank you for reaching out!")
        else:
            messages.success(request, f"{form.errors}")
            print(form.errors)
            
    course = Course.objects.get(id=course_id)
    form = ApplicationForm(initial={'course':course})
    
    context = {
        'form': form,
        'course': course,
    }
    return render(request, "checkout-course.html", context)


@login_required
def submitions(request):
    application_list = Application.objects.filter(user=request.user)

    context = {
        'application_list': application_list,
    }
    return render(request, "applicant/submitions.html", context)
