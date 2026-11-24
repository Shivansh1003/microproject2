from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def home(request):
    return render(request, "homemicroproject.html")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("study")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "login microproject.html")


def signup(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        if name == "" or email == "" or password == "":
            messages.error(request, "Please fill in all fields.")
        elif User.objects.filter(username=email).exists():
            messages.error(request, "An account with this email already exists.")
        else:
            User.objects.create_user(
                username=email,
                email=email,
                first_name=name,
                password=password,
            )
            messages.success(request, "Your account has been created. Please log in.")
            return redirect("login")

    return render(request, "signup microproject.html")


def logout(request):
    auth_logout(request)
    return redirect("login")


def study(request):
    if request.user.is_authenticated == False:
        return redirect("login")

    if request.method == "POST":
        selection = {
            "year": request.POST.get("year", ""),
            "semester": request.POST.get("semester", ""),
            "branch": request.POST.get("branch", ""),
        }
        request.session["study_selection"] = selection
        return redirect("study")

    if request.GET != {}:
        selection = {
            "year": request.GET.get("year", ""),
            "semester": request.GET.get("semester", ""),
            "branch": request.GET.get("branch", ""),
        }
        request.session["study_selection"] = selection
        return redirect("study")

    selection = request.session.get("study_selection", {})
    year = selection.get("year", "")
    semester = selection.get("semester", "")
    branch = selection.get("branch", "")

    course_available = year == "1" and semester == "1" and branch == "aiml"

    selection_attempted = year != "" or semester != "" or branch != ""

    return render(
        request,
        "study.html",
        {
            "selection": selection,
            "course_available": course_available,
            "selection_attempted": selection_attempted,
        },
    )


def show_subject(request, template_name):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, template_name)
