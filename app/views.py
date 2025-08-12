from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def elements(request):
    return render(request, 'elements.html')

def left_sidebar(request):
    return render(request, 'left-sidebar.html')

def right_sidebar(request):
    return render(request, 'right-sidebar.html')

def no_sidebar(request):
    return render(request, 'no-sidebar.html')