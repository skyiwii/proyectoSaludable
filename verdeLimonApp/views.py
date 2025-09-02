from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "verdeLimonTemplates/index.html")

def productos(request):
    return render(request, "verdeLimonTemplates/productos.html")

def nosotros(request):
    return render(request, "verdeLimonTemplates/nosotros.html")

def contacto(request):
    return render(request, "verdeLimonTemplates/contacto.html")

def distribucion(request):
    return render(request, "verdeLimonTemplates/distribucion.html")

