from django.shortcuts import render, redirect

# Create your views here.
def home_page(request):
    return render(request, 'issue_list.html')
