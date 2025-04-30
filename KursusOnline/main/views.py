from django.shortcuts import render

# Create your views here.
def home(request):
    context={}
    return render(request, "main/home.html", context)
def login(request):
    context={}
    return render(request, "main/login.html", context)
def course(request):
    context={}
    return render(request, "main/course.html", context)
def about(request):
    context={}
    return render(request, "main/about.html", context)
def contact(request):
    context={}
    return render(request, "main/contact.html", context)