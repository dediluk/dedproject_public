from django.shortcuts import render

def aboutMe(request):
	return render(request, 'catalog/aboutMe.html')


def index(request):
	return render(request, 'catalog/index.html')
