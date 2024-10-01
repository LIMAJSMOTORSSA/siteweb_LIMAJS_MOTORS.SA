from django.shortcuts import render

# Vue pour le premier template
def index_view(request):
    return render(request, 'index.html')

# Vue pour le deuxième template
def contact_view(request):
    return render(request, 'contact.html')

# Vue pour le troisième template
def about_view(request):
    return render(request, 'about.html')

# Vue pour le quatrième template
def service_view(request):
    return render(request, 'service.html')