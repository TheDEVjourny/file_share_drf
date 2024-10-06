from django.shortcuts import render

# Create your views here.
def home(request):
    # return render(request, 'upload.html')
    return render(request, 'index.html')